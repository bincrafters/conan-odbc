import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class OdbcConan(ConanFile):
    name = 'odbc'
    version = '2.3.5'
    description = 'Package providing unixODBC or Microsoft ODBC'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=False'
    url = 'http://bitbucket-idb:7990/scm/tp/conan-odbc.git'
    license = 'LGPL/GPL'
    source_subfolder = "source_subfolder"
    install_subfolder = "install_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx  # Pure C

    def source(self):
        if self.settings.os == 'Windows':
            return
        v = self.version
        source_url = 'https://iweb.dl.sourceforge.net/project/unixodbc/unixODBC/%s/unixODBC-%s.tar.gz' % (v, v)
        tools.get(source_url)
        extracted_dir = 'unixODBC-%s' % self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        if self.settings.os == 'Windows':
            return
        env_build = AutoToolsBuildEnvironment(self)
        static_flag = 'no' if self.options.shared else 'yes'
        shared_flag = 'yes' if self.options.shared else 'no'
        args = ['--enable-static=%s' % static_flag, '--enable-shared=%s' % shared_flag,
                '--enable-ltdl-install', '--prefix=%s' % os.path.realpath(self.install_subfolder)]
        env_build.configure(configure_dir=self.source_subfolder, args=args)
        env_build.make(args=['-j16'])
        env_build.make(args=['install'])

    def package(self):
        if self.settings.os == 'Windows':
            return
        inc_src = os.path.join(self.install_subfolder, "include")
        lib_src = os.path.join(self.install_subfolder, "lib")
        bin_src = os.path.join(self.install_subfolder, "bin")
        self.copy("LICENSE*", src=self.source_subfolder)
        self.copy("*.h",      dst="include", src=inc_src, keep_path=False)
        self.copy("*.dylib",  dst="lib",     src=lib_src, keep_path=False)
        self.copy("*.so",     dst="lib",     src=lib_src, keep_path=False)
        self.copy("*.so.*",   dst="lib",     src=lib_src, keep_path=False)
        self.copy("*.a",      dst="lib",     src=lib_src, keep_path=False)
        self.copy("*.la",     dst="lib",     src=lib_src, keep_path=False)
        self.copy("*",        dst="bin",     src=bin_src, keep_path=False)

    def package_info(self):
        if self.settings.os == 'Windows':
            self.cpp_info.libs = ['odbc32', 'odbccp32']
        else:
            self.cpp_info.libs = ['odbc', 'odbccr', 'odbcinst', 'ltdl']
