from conans import ConanFile, CMake, tools


class DuktapeConan(ConanFile):
    name = "Duktape"
    version = "2.3.0"
    license = "MIT"
    author = "Sami Vaarala <sami.vaarala@iki.fi>"
    url = "https://duktape.org"
    description = "Duktape is an embeddable Javascript engine, with a focus on portability and compact footprint."
    topics = ("javascript", "engine", "embeddable", "compact")

    def source(self):
        self.run("git clone https://github.com/svaarala/duktape-releases.git")
        self.run("cd duktape-releases && git checkout v%s" % self.version)

    def package(self):
        self.copy("*.h", dst="include", src="duktape-releases/src" )
        self.copy("*.c", dst="src", src="duktape-releases/src" )
        self.copy("*.json", dst="src", src="duktape-releases/src" )

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.srcdirs = ['src']

