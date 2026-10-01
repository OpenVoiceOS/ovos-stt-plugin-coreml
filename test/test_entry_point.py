"""The declared entry point must resolve in the installed environment.

The package declared `coremltools` and `numpy` nowhere, and imports both at
module level, so `find_plugins("opm.stt")` returned nothing for this plugin on
every install. The build only built and installed the package, which succeeds
while the import fails, so nothing said so.

These tests read the metadata of the installed package and then load what the
metadata names. They fail when a requirement the module imports is not
declared.
"""
import unittest
from importlib.metadata import entry_points

GROUP = "opm.stt"
NAME = "ovos-stt-plugin-coreml"


class TestEntryPoint(unittest.TestCase):
    def _entry_point(self):
        found = [e for e in entry_points(group=GROUP) if e.name == NAME]
        self.assertEqual(len(found), 1,
                         f"{NAME} is not registered under {GROUP}")
        return found[0]

    def test_entry_point_is_registered(self):
        self.assertEqual(self._entry_point().value,
                         "ovos_stt_plugin_coreml:CoremlSTT")

    def test_entry_point_loads(self):
        # load() imports the module and reads the attribute, so an undeclared
        # requirement raises here
        self.assertTrue(callable(self._entry_point().load()))

    def test_opm_finds_the_plugin(self):
        # the loader a deployment uses, not importlib alone
        from ovos_plugin_manager.utils import PluginTypes, find_plugins
        self.assertIn(NAME, find_plugins(PluginTypes.STT))

    def test_the_class_is_an_stt(self):
        from ovos_plugin_manager.templates.stt import STT
        from ovos_stt_plugin_coreml import CoremlSTT
        self.assertTrue(issubclass(CoremlSTT, STT))


if __name__ == "__main__":
    unittest.main()
