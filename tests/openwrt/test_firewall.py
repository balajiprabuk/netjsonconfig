import textwrap
import unittest

from netjsonconfig import OpenWrt
from netjsonconfig.exceptions import ValidationError
from netjsonconfig.utils import _TabsMixin


class TestFirewall(unittest.TestCase, _TabsMixin):
    maxDiff = None

    _rule_1_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-MLD",
                    "src": "wan",
                    "src_ip": "fe80::/10",
                    "proto": ["icmp"],
                    "icmp_type": ["130/0", "131/0", "132/0", "143/0"],
                    "target": "ACCEPT",
                    "family": "ipv6",
                }
            ]
        }
    }

    _rule_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_MLD'
            option name 'Allow-MLD'
            option src 'wan'
            option src_ip 'fe80::/10'
            option proto 'icmp'
            list icmp_type '130/0'
            list icmp_type '131/0'
            list icmp_type '132/0'
            list icmp_type '143/0'
            option target 'ACCEPT'
            option family 'ipv6'
        """
    )

    def test_render_rule_1(self):
        o = OpenWrt(self._rule_1_netjson)
        expected = self._tabs(self._rule_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_1(self):
        o = OpenWrt(native=self._rule_1_uci)
        self.assertEqual(o.config, self._rule_1_netjson)

    _rule_2_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-DHCPv6",
                    "src": "wan",
                    "src_ip": "fc00::/6",
                    "dest_ip": "fc00::/6",
                    "dest_port": "546",
                    "proto": ["udp"],
                    "target": "ACCEPT",
                    "family": "ipv6",
                }
            ]
        }
    }

    _rule_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_DHCPv6'
            option name 'Allow-DHCPv6'
            option src 'wan'
            option src_ip 'fc00::/6'
            option dest_ip 'fc00::/6'
            option dest_port '546'
            option proto 'udp'
            option target 'ACCEPT'
            option family 'ipv6'
        """
    )

    def test_render_rule_2(self):
        o = OpenWrt(self._rule_2_netjson)
        expected = self._tabs(self._rule_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_2(self):
        o = OpenWrt(native=self._rule_2_uci)
        self.assertEqual(o.config, self._rule_2_netjson)

    _rule_3_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-Ping",
                    "src": "wan",
                    "proto": ["icmp"],
                    "family": "ipv4",
                    "icmp_type": ["echo-request"],
                    "target": "ACCEPT",
                    "enabled": False,
                }
            ]
        }
    }

    _rule_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_Ping'
            option name 'Allow-Ping'
            option src 'wan'
            option proto 'icmp'
            option family 'ipv4'
            list icmp_type 'echo-request'
            option target 'ACCEPT'
            option enabled '0'
        """
    )

    def test_render_rule_3(self):
        o = OpenWrt(self._rule_3_netjson)
        expected = self._tabs(self._rule_3_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_3(self):
        o = OpenWrt(native=self._rule_3_uci)
        self.assertEqual(o.config, self._rule_3_netjson)

    _rule_4_netjson = {
        "firewall": {
            "rules": [
                {
                    "name": "Allow-Isolated-DHCP",
                    "src": "isolated",
                    "proto": ["udp"],
                    "dest_port": "67-68",
                    "target": "ACCEPT",
                }
            ]
        }
    }

    _rule_4_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config rule 'rule_Allow_Isolated_DHCP'
            option name 'Allow-Isolated-DHCP'
            option src 'isolated'
            option proto 'udp'
            option dest_port '67-68'
            option target 'ACCEPT'
        """
    )

    def test_render_rule_4(self):
        o = OpenWrt(self._rule_4_netjson)
        expected = self._tabs(self._rule_4_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_rule_4(self):
        o = OpenWrt(native=self._rule_4_uci)
        self.assertEqual(o.config, self._rule_4_netjson)

    _zone_1_netjson = {
        "firewall": {
            "zones": [
                {
                    "name": "lan",
                    "input": "ACCEPT",
                    "output": "ACCEPT",
                    "forward": "ACCEPT",
                    "network": ["lan"],
                    "mtu_fix": True,
                }
            ]
        }
    }

    _zone_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config zone 'zone_lan'
            option name 'lan'
            option input 'ACCEPT'
            option output 'ACCEPT'
            option forward 'ACCEPT'
            option network 'lan'
            option mtu_fix '1'
        """
    )

    def test_render_zone_1(self):
        o = OpenWrt(self._zone_1_netjson)
        expected = self._tabs(self._zone_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_zone_1(self):
        o = OpenWrt(native=self._zone_1_uci)
        self.assertEqual(o.config, self._zone_1_netjson)

    _zone_2_netjson = {
        "firewall": {
            "zones": [
                {
                    "name": "wan",
                    "input": "DROP",
                    "output": "ACCEPT",
                    "forward": "DROP",
                    "network": ["wan", "wan6"],
                    "mtu_fix": True,
                    "masq": True,
                }
            ]
        }
    }

    _zone_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config zone 'zone_wan'
            option name 'wan'
            option input 'DROP'
            option output 'ACCEPT'
            option forward 'DROP'
            list network 'wan'
            list network 'wan6'
            option mtu_fix '1'
            option masq '1'
        """
    )

    # This one is the same as _zone_2_uci with the exception that the "network"
    # parameter is specified as a single string.
    _zone_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config zone 'zone_wan'
            option name 'wan'
            option input 'DROP'
            option output 'ACCEPT'
            option forward 'DROP'
            option network 'wan wan6'
            option mtu_fix '1'
            option masq '1'
        """
    )

    def test_render_zone_2(self):
        o = OpenWrt(self._zone_2_netjson)
        expected = self._tabs(self._zone_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_zone_2(self):
        o = OpenWrt(native=self._zone_2_uci)
        self.assertEqual(o.config, self._zone_2_netjson)

    def test_parse_zone_3(self):
        o = OpenWrt(native=self._zone_3_uci)
        self.assertEqual(o.config, self._zone_2_netjson)

    _forwarding_1_netjson = {
        "firewall": {"forwardings": [{"src": "isolated", "dest": "wan"}]}
    }

    _forwarding_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'forwarding_isolated_wan'
            option src 'isolated'
            option dest 'wan'
        """
    )

    def test_render_forwarding_1(self):
        o = OpenWrt(self._forwarding_1_netjson)
        expected = self._tabs(self._forwarding_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_1(self):
        o = OpenWrt(native=self._forwarding_1_uci)
        self.assertEqual(o.config, self._forwarding_1_netjson)

    _forwarding_2_netjson = {
        "firewall": {
            "forwardings": [{"src": "isolated", "dest": "wan", "family": "ipv4"}]
        }
    }

    _forwarding_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'forwarding_isolated_wan_ipv4'
            option src 'isolated'
            option dest 'wan'
            option family 'ipv4'
        """
    )

    def test_render_forwarding_2(self):
        o = OpenWrt(self._forwarding_2_netjson)
        expected = self._tabs(self._forwarding_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_2(self):
        o = OpenWrt(native=self._forwarding_2_uci)
        self.assertEqual(o.config, self._forwarding_2_netjson)

    _forwarding_3_netjson = {
        "firewall": {"forwardings": [{"src": "lan", "dest": "wan", "family": "any"}]}
    }

    _forwarding_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config forwarding 'forwarding_lan_wan_any'
            option src 'lan'
            option dest 'wan'
            option family 'any'
        """
    )

    def test_render_forwarding_3(self):
        o = OpenWrt(self._forwarding_3_netjson)
        expected = self._tabs(self._forwarding_3_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_forwarding_3(self):
        o = OpenWrt(native=self._forwarding_3_uci)
        self.assertEqual(o.config, self._forwarding_3_netjson)

    def test_forwarding_validation_error(self):
        o = OpenWrt(
            {
                "firewall": {
                    "forwardings": [{"src": "lan", "dest": "wan", "family": "XXXXXX"}]
                }
            }
        )
        with self.assertRaises(ValidationError):
            o.validate()

    _redirect_1_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                }
            ]
        }
    }

    _redirect_1_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'redirect_Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
        """
    )

    def test_render_redirect_1(self):
        o = OpenWrt(self._redirect_1_netjson)
        expected = self._tabs(self._redirect_1_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_redirect_1(self):
        o = OpenWrt(native=self._redirect_1_uci)
        self.assertEqual(o.config, self._redirect_1_netjson)

    _redirect_2_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                    # Contrived, unrealistic example for testing
                    "weekdays": ["mon", "tue", "wed"],
                    "monthdays": [1, 2, 3, 29, 30],
                }
            ]
        }
    }

    _redirect_2_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'redirect_Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
            list weekdays 'mon'
            list weekdays 'tue'
            list weekdays 'wed'
            list monthdays '1'
            list monthdays '2'
            list monthdays '3'
            list monthdays '29'
            list monthdays '30'
        """
    )

    def test_render_redirect_2(self):
        o = OpenWrt(self._redirect_2_netjson)
        expected = self._tabs(self._redirect_2_uci)
        self.assertEqual(o.render(), expected)

    def test_parse_redirect_2(self):
        o = OpenWrt(native=self._redirect_2_uci)
        self.assertEqual(o.config, self._redirect_2_netjson)

    def test_redirect_weekdays_validation_error_1(self):
        o = OpenWrt({"firewall": {"redirects": [{"weekdays": ["mon", "xxx"]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_redirect_weekdays_validation_error_2(self):
        o = OpenWrt({"firewall": {"redirects": [{"weekdays": ["mon", 1]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_redirect_monthdays_validation_error_1(self):
        o = OpenWrt({"firewall": {"redirects": [{"monthdays": [2, 8, 32]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    def test_redirect_monthdays_validation_error_2(self):
        o = OpenWrt({"firewall": {"redirects": [{"monthdays": [0, 2, 8]}]}})
        with self.assertRaises(ValidationError):
            o.validate()

    _redirect_3_uci = textwrap.dedent(
        """\
        package firewall

        config defaults 'defaults'

        config redirect 'redirect_Adblock DNS, port 53'
            option name 'Adblock DNS, port 53'
            option src 'lan'
            option proto 'tcpudp'
            option src_dport '53'
            option dest_port '53'
            option target 'DNAT'
            option weekdays '! mon tue wed'
            option monthdays '! 1 2 3 4 5'
        """
    )

    _redirect_3_netjson = {
        "firewall": {
            "redirects": [
                {
                    "name": "Adblock DNS, port 53",
                    "src": "lan",
                    "proto": ["tcp", "udp"],
                    "src_dport": "53",
                    "dest_port": "53",
                    "target": "DNAT",
                    "weekdays": ["sun", "thu", "fri", "sat"],
                    "monthdays": [
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31,
                    ],
                }
            ]
        }
    }

    def test_parse_redirect_3(self):
        o = OpenWrt(native=self._redirect_3_uci)
        print(o.config)
        self.assertEqual(o.config, self._redirect_3_netjson)