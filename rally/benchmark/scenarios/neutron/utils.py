# Copyright 2014: Intel Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import multiprocessing

import netaddr

from rally.benchmark.scenarios import base
from rally.benchmark.scenarios import utils as scenario_utils


class NeutronScenario(base.Scenario):
    """This class should contain base operations for benchmarking neutron."""

    RESOURCE_NAME_PREFIX = "rally_net_"
    SUBNET_IP_VERSION = 4
    SUBNET_CIDR_START = "1.1.0.0/30"

    _subnet_cidrs = {}

    @classmethod
    def _generate_subnet_cidr(cls, network_id):
        """Generate next subnet CIDR for network, without IP overlapping.

        :param network_id: str, network UUID for subnet
        :returns: str, next available subnet CIDR
        """
        with multiprocessing.Lock():
            if network_id in cls._subnet_cidrs:
                crnt_cidr = cls._subnet_cidrs[network_id]
                cidr = str(netaddr.IPNetwork(crnt_cidr).next())
            else:
                cidr = str(netaddr.IPNetwork(cls.SUBNET_CIDR_START))
        cls._subnet_cidrs[network_id] = cidr
        return cidr

    @scenario_utils.atomic_action_timer('neutron.create_network')
    def _create_network(self, network_create_args):
        """Create neutron network.

        :param network_create_args: dict, POST /v2.0/networks request options
        :returns: neutron network dict
        """
        network_create_args.setdefault("name", self._generate_random_name())
        return self.clients("neutron"
                            ).create_network({"network": network_create_args})

    @scenario_utils.atomic_action_timer('neutron.list_networks')
    def _list_networks(self):
        """Return user networks list."""
        return self.clients("neutron").list_networks()['networks']

    @scenario_utils.atomic_action_timer('neutron.create_subnet')
    def _create_subnet(self, network, subnet_create_args):
        """Create neutron subnet.

        :param network: neutron network dict
        :param subnet_create_args: POST /v2.0/subnets request options
        :returns: neutron subnet dict
        """
        network_id = network["network"]["id"]
        subnet_create_args["network_id"] = network_id
        subnet_create_args.setdefault(
            "name", self._generate_random_name("rally_subnet_"))
        subnet_create_args.setdefault(
            "cidr", self._generate_subnet_cidr(network_id))
        subnet_create_args.setdefault(
            "ip_version", self.SUBNET_IP_VERSION)

        return self.clients("neutron"
                            ).create_subnet({"subnet": subnet_create_args})

    @scenario_utils.atomic_action_timer('neutron.list_subnets')
    def _list_subnets(self):
        """Returns user subnetworks list."""
        return self.clients("neutron").list_subnets()["subnets"]

    @scenario_utils.atomic_action_timer('neutron.create_router')
    def _create_router(self, router_create_args):
        """Create neutron router.

        :param router_create_args: POST /v2.0/routers request options
        :returns: neutron router dict
        """
        router_create_args.setdefault(
            "name", self._generate_random_name("rally_router_"))
        return self.clients("neutron"
                            ).create_router({"router": router_create_args})

    @scenario_utils.atomic_action_timer('neutron.list_routers')
    def _list_routers(self):
        """Returns user routers list."""
        return self.clients("neutron").list_routers()["routers"]
