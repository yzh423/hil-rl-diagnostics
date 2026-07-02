import os
import unittest

from foresight_hil.envs.robosuite_env import _ensure_numba_cache_dir


class RobosuiteStartupConfigTest(unittest.TestCase):
    def test_numba_cache_defaults_to_project_local_dir(self):
        old = os.environ.pop("NUMBA_CACHE_DIR", None)
        try:
            cache_dir = _ensure_numba_cache_dir()
            self.assertTrue(cache_dir.endswith(".numba_cache"))
            self.assertTrue(os.path.isdir(cache_dir))
        finally:
            if old is None:
                os.environ.pop("NUMBA_CACHE_DIR", None)
            else:
                os.environ["NUMBA_CACHE_DIR"] = old

    def test_existing_numba_cache_dir_is_preserved(self):
        old = os.environ.get("NUMBA_CACHE_DIR")
        os.environ["NUMBA_CACHE_DIR"] = "custom-cache-dir"
        try:
            self.assertEqual(_ensure_numba_cache_dir(), "custom-cache-dir")
        finally:
            if old is None:
                os.environ.pop("NUMBA_CACHE_DIR", None)
            else:
                os.environ["NUMBA_CACHE_DIR"] = old


if __name__ == "__main__":
    unittest.main()
