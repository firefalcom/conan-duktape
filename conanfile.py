from conan import ConanFile
from conan.tools.files import copy
from os.path import join

class DuktapeConan(ConanFile):
    name = "duktape"
    version = "2.7.0-2"

    license = "MIT"
    author = "Sami Vaarala <sami.vaarala@iki.fi>"
    url = "https://duktape.org"
    description = "Duktape is an embeddable Javascript engine, with a focus on portability and compact footprint."
    topics = ("javascript", "engine", "embeddable", "compact")

    options = {
        "with_debugger": [False, True],
        "fatal_handler": [None,"ANY"],
        "manual_gc": [False, True],
        "use_exception": [False, True],

    }

    default_options = {
        "with_debugger": False,
        "fatal_handler": None,
        "manual_gc": False,
        "use_exception" : False,
        }

    def source(self):
        duktape_version = self.version.split('-')[0]
        self.run("git clone https://github.com/svaarala/duktape-releases.git")
        self.run("cd duktape-releases && git checkout v%s" % duktape_version)
        copy(self, "tools/*", self.export_sources_folder, join(self.export_sources_folder, "duktape-releases/"))
        copy(self, "custom_config/*", self.export_sources_folder, join(self.export_sources_folder, "duktape-releases/config/helper-snippets/"), keep_path=False)

    def export_sources(self):
        copy(self, "tools/*", self.recipe_folder, self.export_sources_folder)
        copy(self, "custom_config/*", self.recipe_folder, self.export_sources_folder)

    def package(self):
        configuration_string = ""

        if self.options.with_debugger:
            configuration_string = configuration_string + (
                "-DDUK_USE_DEBUGGER_SUPPORT -DDUK_USE_INTERRUPT_COUNTER " +
                "-DDUK_USE_DEBUGGER_DUMPHEAP -DDUK_USE_DEBUGGER_FWD_LOGGING " +
                "-DDUK_USE_DEBUGGER_FWD_PRINTALERT -DDUK_USE_DEBUGGER_INSPECT " +
                "-DDUK_USE_DEBUGGER_PAUSE_UNCAUGHT -DDUK_USE_DEBUGGER_THROW_NOTIFY ")

        if self.options.get_safe("fatal_handler"):
            configuration_string = configuration_string + " -DDUK_USE_FATAL_HANDLER=" + str(self.options.fatal_handler)

        if self.options.manual_gc:
            configuration_string = configuration_string + (
                "-DDUK_USE_MARK_AND_SWEEP "
                "-DDUK_USE_REFERENCE_COUNTING "
                "-UDUK_USE_VOLUNTARY_GC " )

        if self.options.use_exception:
            configuration_string = configuration_string + "-DDUK_USE_CPP_EXCEPTIONS "

        self.run("python3 -Xutf8 duktape-releases/tools/configure.py --output-directory generated/ "
            + " --source-directory duktape-releases/src-input --config-metadata duktape-releases/config "
            + configuration_string)

        copy(self, "*.h", join(self.source_folder, "generated"), join(self.package_folder, "include"))
        copy(self, "*.c", join(self.source_folder, "generated"), join(self.package_folder, "src"))
        copy(self, "*.json", join(self.source_folder, "generated"), join(self.package_folder, "src"))

        if self.options.with_debugger:
            copy(self, "*.h", join(self.source_folder, "duktape-releases/examples/debug-trans-socket/"), join(self.package_folder, "include"))
            copy(self, "*.c", join(self.source_folder, "duktape-releases/examples/debug-trans-socket/"), join(self.package_folder, "src"))


    def package_id(self):
        self.info.settings.clear()

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.srcdirs = ['src']
