"""Module containing the tests for the default scenario."""

import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["nvme-cli"])
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize(
    "file,content",
    [("/etc/modprobe.d/nvme_core.conf", r"^options nvme_core io_timeout=[0-9]*$")],
)
def test_files_content(host, file, content):
    """Test that config files were modified as expected."""
    f = host.file(file)

    # This kernel configuration setting is already present in Amazon Linux
    if host.system_info.distribution != "amzn":
        assert f.exists
        assert f.contains(content)
