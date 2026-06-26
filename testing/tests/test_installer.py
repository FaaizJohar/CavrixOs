import pytest
import sys
import os
import subprocess
from unittest.mock import patch, MagicMock

# Add installer source to path for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../installer/src')))

from fs.btrfs import BtrfsManager
from security.luks import LUKSManager
from boot.uki import UKIManager

@patch('subprocess.run')
def test_btrfs_partition_disk(mock_run):
    """Verifies that the disk is partitioned correctly via parted."""
    mock_run.return_value = MagicMock(returncode=0)
    btrfs = BtrfsManager("/dev/mockdisk", "/mnt")
    
    result = btrfs.partition_disk()
    assert result is True
    
    # Verify the commands executed
    calls = mock_run.call_args_list
    assert ["umount", "-q", "-f", "/dev/mockdisk*"] in [c[0][0] for c in calls]
    assert ["parted", "-s", "/dev/mockdisk", "mklabel", "gpt"] in [c[0][0] for c in calls]
    assert ["parted", "-s", "/dev/mockdisk", "mkpart", "ESP", "fat32", "1MiB", "1025MiB"] in [c[0][0] for c in calls]

@patch('subprocess.Popen')
def test_luks_encryption_failure(mock_popen):
    """Verifies that LUKS encryption gracefully handles cryptsetup failures."""
    mock_process = MagicMock()
    mock_process.communicate.return_value = (b"", b"Device or resource busy")
    mock_process.returncode = 1
    mock_popen.return_value = mock_process
    
    luks = LUKSManager("/dev/mockdisk2")
    result = luks.encrypt_partition("testpass")
    
    assert result is False
    mock_popen.assert_called_once_with(
        ["cryptsetup", "-q", "luksFormat", "--type", "luks2", "/dev/mockdisk2"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

@patch('subprocess.run')
def test_uki_generation(mock_run):
    """Verifies mkinitcpio presets are generated and compiled correctly."""
    mock_run.return_value = MagicMock(returncode=0)
    uki = UKIManager("/mnt")
    
    # We mock open to avoid writing to host disk during testing
    with patch("builtins.open", MagicMock()) as mock_file:
        assert uki.write_loader_conf() is True
        assert uki.configure_mkinitcpio_uki("linux-zen") is True
        assert uki.generate_cmdline("mock-uuid", is_encrypted=True) is True
        
    # Verify mkinitcpio execution
    assert uki.generate_ukis() is True
    mock_run.assert_called_with(["arch-chroot", "/mnt", "mkinitcpio", "-P"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
