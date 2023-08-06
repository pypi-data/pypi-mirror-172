import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.6.0.post153"
version_tuple = (0, 6, 0, 153)
try:
    from packaging.version import Version as V
    pversion = V("0.6.0.post153")
except ImportError:
    pass

# Data version info
data_version_str = "0.6.0.post11"
data_version_tuple = (0, 6, 0, 11)
try:
    from packaging.version import Version as V
    pdata_version = V("0.6.0.post11")
except ImportError:
    pass
data_git_hash = "642cfb2f20825677916c2abc8410e242ff4eb450"
data_git_describe = "0.6.0-11-g642cfb2f"
data_git_msg = """\
commit 642cfb2f20825677916c2abc8410e242ff4eb450
Merge: 42281285 1721994b
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Thu Oct 20 12:31:42 2022 +0200

    Merge pull request #691 from silabs-oysteink/zero-replicate-fixes
    
    Removed possible zero-replication code

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
