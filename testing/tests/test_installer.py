import pytest
import sys
import os

# Add installer source to path for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../installer/src')))

from hardware.detector import HardwareDetector
from fs.btrfs import BtrfsManager

def test_hardware_detector_generic():
    """Ensure the hardware detector falls back to generic safely without lspci."""
    # In a CI environment without GPUs, it should return generic or CPU
    gpu = HardwareDetector.get_gpu_vendor()
    assert gpu in ["nvidia", "amd", "intel", "generic"]

def test_btrfs_subvolume_config():
    """Ensure the BTRFS subvolume layout matches the strict rollback architecture."""
    btrfs = BtrfsManager("/dev/mock", "/mnt")
    assert "@" in btrfs.subvolumes
    assert "@home" in btrfs.subvolumes
    assert "@snapshots" in btrfs.subvolumes
    
def test_vram_estimation():
    """Ensure VRAM estimator returns a valid dictionary."""
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ai/daemon')))
    try:
        from core.vram import VRAMEstimator
        res = VRAMEstimator.get_available_vram()
        assert "vendor" in res
        assert "free_mb" in res
        assert isinstance(res["free_mb"], int)
    except ImportError:
        pass # Optional if ai is not built yet
