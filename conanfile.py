from conans import ConanFile, CMake, tools


class opendnp3Conan(ConanFile):
    name = "opendnp3"
    version = "3.1.1"
    commit = version
    license = "Apache 2.0"
    author = "Vladislav Troinich antlad@icloud.com"
    url = "https://github.com/dnp3/opendnp3"
    description = "DNP3 (IEEE-1815) protocol stack."
    topics = ("opcua")
    settings = "cppstd", "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    build_policy = "missing"

    requires = (
        "openssl/1.1.1d",
    )

    def source(self):
        self.run(
            "git clone https://github.com/dnp3/opendnp3 && cd opendnp3 && git checkout {}".format(self.version))

    def build(self):
        cmake = CMake(self)
        static_build = "ON"
        if self.options["shared"]:  # e.g. if self.options.myoption:
            static_build = "OFF"
        cmake.definitions["DNP3_STATIC_LIBS"] = static_build
        cmake.configure(source_dir="opendnp3", args=[])
        cmake.build()

    def package(self):

        self.run("ls opendnp3/cpp/lib/include")

        self.copy("*.h", dst="./include/",
                  src="opendnp3/cpp/lib/include/", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["opendnp3"]
        self.cpp_info.includedirs = ['./include/']
