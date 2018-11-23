from conans import ConanFile, CMake, RunEnvironment, tools
import os


class FalconTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", "bin", "bin")

    def test(self):
        os.chdir("bin")
        self.run(os.path.join('.', 'example'))

        self.run('odbcinst --version', run_environment=True)
