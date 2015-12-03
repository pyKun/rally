============
Rally v0.1.2
============

Information
-----------

+------------------+-----------------------+
| Commits          |        **162**        |
+------------------+-----------------------+
| Bug fixes        |        **22**         |
+------------------+-----------------------+
| Dev cycle        |      **58 days**      |
+------------------+-----------------------+
| Release date     |  **3/December/2015**  |
+------------------+-----------------------+


Details
-------

This release, as well as all previous ones, includes a lot of internal and
external changes. Most important are listed below.

* Blueprint consistent-resource-names_: Resource name is based on Task id now.
  It is a huge step to persistence and disaster cleanups.
* It is much easier to view rally reports on machines without internet
  connection now. We add new option "html-static" to "rally task report"
  cmd, which puts static js/css files near report.
* Class `rally.common.objects.Endpoint` was renamed to `Credentials`. Old
  class is kept for backward compatibility. Please, stop using the old class
  in your plugins.
* We refused to use mako templates in favour to jinja2. Such change didn't
  touch you in the short term, but jinja2 gives ability to add more interesting
  features in our reports easier.

.. warning:: Release 0.1.2 is the last release with Python 2.6 support.

New Features
~~~~~~~~~~~~

* Certification task: neutron checks
* Add CobblerProvider
* Added possibility to run Tempest tests listed in a file
* Added possibility to upload Tempest subunit stream logs into data base
* Improved tempest support:
 * Improvements in generating Tempest config file
 * Reworked subunit stream parser
 * Rally team tries to simplify usage of each our components. Rally verification
   acquired come kind of context as in Tasks. Before launching each verification,
   Rally checks existence of required resources(networks, images, flavours etc)
   in tempest configuration file and pre-creates them. Do not worry, all these
   resources will not be forgotten and left, Rally will clean them all after
   verification.

API Changes
~~~~~~~~~~~~

New api methods were added:
 * Task.create_template_functions
 * Verification.show_config_info
 * Verification.list
 * Verification.get
 * Deployment.list
 * Deployment.check


Specs & Feature requests
~~~~~~~~~~~~~~~~~~~~~~~~

* Add a spec for distiributed load generation
* Propose improvements for scenario output format
* Task and verification export

Plugins
~~~~~~~

Move rally.osclients.Clients to plugin base

* **Scenarios**:

 * LBaaS V1 healthmonitor scenarios
 * Add Neutron Security Groups scenarios
 * Add boot-server-attach-created-volume-and-resize nova benchmark
 * Support for Designate V2 api
 * New Swift Scenarios:

    - list_and_download_objects_in_containers
    - list_objects_in_containers

 * A lot of improvements in Sahara scenarios
 * New context was added - api_versions. It allows to setup client to communicate to specific service.

Usage example #1(setting api version and service name to communicate):

.. code:: none

  CinderVolumes.create_and_delete_volume:
    -
      args:
        size: 1
      runner:
        type: "constant"
        times: 2
        concurrency: 2
      context:
        users:
          tenants: 2
          users_per_tenant: 2
        api_versions:
          cinder:
            version: 2
            service_name: cinderv2

Usage example #2 - setting api version and service type to cumminicate:

.. code:: none

  CinderVolumes.create_and_delete_volume:
    -
      args:
        size: 1
      runner:
        type: "constant"
        times: 2
        concurrency: 2
      context:
        users:
          tenants: 2
          users_per_tenant: 2
        api_versions:
          cinder:
            version: 2
            service_type: volumev2

Bug fixes
~~~~~~~~~

**22 bugs were fixed, the most critical are**:

* Follow symlinks in plugin discovery
* Use sed without -i option for portability (install_rally.sh)
* Fixed race in rally.common.broker
* Fixed incorrect iteration number on "Failures" Tab

Documentation
~~~~~~~~~~~~~

Fixed some minor typos and inaccuracies.

.. _consistent-resource-names: https://blueprints.launchpad.net/rally/+spec/consistent-resource-names
