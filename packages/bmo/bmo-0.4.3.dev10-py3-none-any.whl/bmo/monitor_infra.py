#!/usr/bin/env python

import typing as T
import pydig

from functools import lru_cache
from pathlib import Path
from collections import defaultdict

import sqlite3 as db
import datetime
import csv
import logging

import pprint

_print = pprint.pprint

import nmap3

g_nmap_client = nmap3.Nmap()

CHECK_METHOD = ""
DATA = {}
VALUE = 0


def csv2dicts(csvinfo) -> T.List[T.Dict[str, T.Any]]:
    return list(csv.DictReader(csvinfo.splitlines(), delimiter=";"))


class MonitorDatabase:
    def __init__(self, dbpath: Path):
        # connecting to sqlite database
        self.connection = db.connect(str(dbpath))
        self.cursor = self.connection.cursor()
        self.table_name: T.Final[str] = "asset_connectivity"
        query = f"""
        create table if not exists {self.table_name} (
            unix_epoch_ms DATETIME,
            url VARCHAR(64),
            check_method VARCHAR(64),
            details_json VARCHAR(1024),
            value INTEGER(2)
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def execute(self, query, data):
        try:
            self.cursor.execute(query, data)
        except Exception as e:
            logging.error(f"Failed. Query was '{query}'. Error {e}")
            quit(1)

    def insert_info(self, url, check_mathod, DATA, VALUE):
        timestamp = datetime.datetime.now()
        query_add_data = f"INSERT INTO {self.table_name} VALUES(?,?,?,?,?)"
        self.execute(query_add_data, (timestamp, url, check_mathod, str(DATA), VALUE))

        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


# functions for 'resource' variable
@lru_cache
def dig_url_address(url: str) -> T.List[str]:
    if url.find("//") >= 0:
        url = url.split("//")[1]
    return pydig.query(url, "A")


@lru_cache
def port_information(ipaddr) -> T.List[T.Dict[str, str]]:
    global g_nmap_client

    ports_info = g_nmap_client.scan_top_ports(ipaddr)[ipaddr]["ports"]
    assert ports_info
    return ports_info


def check_port(port_info, ports, url, db):
    global CHECK_METHOD, DATA, VALUE

    CHECK_METHOD = "port_status"
    open_ports = []
    for info in port_info.values():
        for data in info:
            if data["state"] == "open":
                open_ports.append(data["portid"])
    for port in ports:
        DATA["id"] = port
        if port in open_ports:
            VALUE = 1
            db.insert_info(url, CHECK_METHOD, DATA, VALUE)
        else:
            VALUE = 0
            db.insert_info(url, CHECK_METHOD, DATA, VALUE)


def api_information(url, method, endpoint, db):
    import requests

    global CHECK_METHOD, DATA, VALUE

    CHECK_METHOD = "api_status"
    DATA["endpoint"] = endpoint
    DATA["method"] = method.upper()
    url_with_endpoint = url + endpoint
    if method == "get":
        response = requests.get(url_with_endpoint)
        if response.status_code == 200:
            VALUE = 1
            db.insert_info(url, CHECK_METHOD, DATA, VALUE)
        else:
            VALUE = 0
            db.insert_info(url, CHECK_METHOD, DATA, VALUE)
    elif method == "post":
        response = requests.post(url_with_endpoint)
        if response.status_code == 200:
            VALUE = 1
            db.insert_info(url, CHECK_METHOD, DATA, VALUE)
        else:
            VALUE = 0
            db.insert_info(url, CHECK_METHOD, DATA, VALUE)


def url_to_ipaddress(url: str) -> T.List[str]:
    assert url
    return dig_url_address(url)


def check_str(url: str, method: str, db, **kwargs):
    # TODO: Make sure url is consistent
    if method == "opened_ports" or method == "closed_ports":
        results = dict()
        ports = kwargs["ports"]
        assert ports
        for addr in url_to_ipaddress(url):
            addr = addr.rstrip()
            results[addr] = port_information(addr)
            DATA["address"] = addr
            check_port(results, ports, url, db)

    elif method == "get" or method == "post":
        results = dict()
        endpoint = kwargs["endpoint"]
        for addr in url_to_ipaddress(url):
            addr = addr.rstrip()
            api_information(url, method, endpoint, db)

    else:
        raise RuntimeError(f"{method=} is not implemented")


# functions for 'check' and 'args' variable


def method_get(resource: str, db, *args):
    logging.info(f"Checking get {resource}:{args}")
    check_str(resource, "get", db, endpoint=args[0] if args else "")


def method_post(resource: str, db, *args):
    logging.info(f"Checking post {resource}:{args}")
    check_str(resource, "post", db, endpoint=args[0] if args else "")


def method_opened_ports(resource, db, *ports):
    logging.info(f"Checking opened_ports {resource} {','.join(ports)}")
    check_str(resource, "opened_ports", db, ports=ports)


def method_closed_ports(resource, db, *ports):
    logging.info(f"Checking closed_ports {resource}:{ports}")
    check_str(resource, "closed_ports", db, ports=ports)


def check_resource(
    resource: str,
    *,
    method: str,
    args: T.List[str] = [],
    db_path: Path = Path("_monitor.db"),
) -> T.Tuple[T.Dict[T.Any, T.Any], int]:
    """Monitor a list of url/ip."""
    global DATA, VALUE
    DATA = {}
    VALUE = 0
    db = MonitorDatabase(db_path)
    func = globals().get(f"method_{method}")
    if func is not None:
        func(resource, db, *args)
    else:
        available = [
            x.replace("method_", "") for x in globals().keys() if "method_" in x
        ]
        logging.warning(f"[Warn] {method} is not supported. Available are {available}")
    db.close()

    # TODO: Retrun the added entries in human redable format.
    return (DATA, VALUE)


def monitor_infra(resource_file: Path):
    """Monitor infrastructure given in a file"""
    logging.info(f"Readin from {resource_file}.")
    for line in resource_file.read_text().splitlines():
        fs = line.split(";")
        if not fs:
            continue
        resource = fs[0]
        method = fs[1] if len(fs) > 1 else "get"
        args = fs[2].split(",") if len(fs) > 2 else []
        check_resource(resource, method=method, args=args)
