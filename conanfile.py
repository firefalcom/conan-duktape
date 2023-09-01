from conans import ConanFile, CMake, tools
from conan.tools.files import copy
import os


class DuktapeConan(ConanFile):
    name = "Duktape"
    version = "2.7.0-1"
    license = "MIT"
    author = "Sami Vaarala <sami.vaarala@iki.fi>"
    url = "https://duktape.org"
    description = "Duktape is an embeddable Javascript engine, with a focus on portability and compact footprint."
    topics = ("javascript", "engine", "embeddable", "compact")

    exports_sources = {"tools/*"}

    options = {
        "with_debugger": [False, True],
        "fatal_handler": "ANY",
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
        copy(self, "tools/*", self.export_sources_folder, os.path.join(self.export_sources_folder, "duktape-releases/"))

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

        if configuration_string != "":
            self.run("python3 duktape-releases/tools/configure.py --output-directory generated/ "
               + " --source-directory duktape-releases/src-input --config-metadata duktape-releases/config "
               + configuration_string)
            self.copy("*.h", dst="include", src="generated" )
            self.copy("*.c", dst="src", src="generated" )
            self.copy("*.json", dst="src", src="generated" )
        else:
            self.copy("*.h", dst="include", src="duktape-releases/src" )
            self.copy("*.c", dst="src", src="duktape-releases/src" )
            self.copy("*.json", dst="src", src="duktape-releases/src" )

        if self.options.with_debugger:
            self.copy("*.h", dst="include", src="duktape-releases/examples/debug-trans-socket/" )
            self.copy("*.c", dst="src", src="duktape-releases/examples/debug-trans-socket/" )

    def package_id(self):
        del self.info.settings.compiler
        del self.info.options.os
        del self.info.options.arch
        del self.info.options.build_type

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.srcdirs = ['src']

