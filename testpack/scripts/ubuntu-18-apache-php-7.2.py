#!/usr/bin/env python3

import unittest
import os
import docker
from selenium import webdriver
import os.path
import tarfile
from io import BytesIO
import time


class Test1and1ApacheImage(unittest.TestCase):
    container = None
    container_ip = None

    @classmethod
    def setUpClass(cls):
        image_to_test = os.getenv("IMAGE_NAME")
        if image_to_test == "":
            raise Exception("I don't know what image to test")

        client = docker.from_env()
        Test1and1ApacheImage.container = client.containers.run(
            image=image_to_test,
            remove=True,
            detach=True,
            network_mode="bridge",
            user=10000,
            ports={8080:8080}
        )
        Test1and1ApacheImage.copy_test_files("testpack/files", "html", "/var/www")

        details = docker.APIClient().inspect_container(container=Test1and1ApacheImage.container.id)
        Test1and1ApacheImage.container_ip = details['NetworkSettings']['IPAddress']

    @classmethod
    def copy_test_files(cls, startfolder, relative_source, dest):
        # Change to the start folder
        pwd = os.getcwd()
        os.chdir(startfolder)
        # Tar up the request folder
        pw_tarstream = BytesIO()
        with tarfile.open(fileobj=pw_tarstream, mode='w:gz') as tf:
            tf.add(relative_source)
        # Copy the archive to the correct destination
        docker.APIClient().put_archive(
            container=Test1and1ApacheImage.container.id,
            path=dest,
            data=pw_tarstream.getvalue()
        )
        # Change back to original folder
        os.chdir(pwd)

    @classmethod
    def tearDownClass(cls):
        Test1and1ApacheImage.container.stop()

    def setUp(self):
        print ("\nIn method", self._testMethodName)
        self.container = Test1and1ApacheImage.container

    def check_success(self, page):
        time.sleep(5)
        driver = webdriver.PhantomJS()
        driver.get("http://%s:8080/%s" % (Test1and1ApacheImage.container_ip, page))
        self.assertTrue(
            driver.page_source.find('Success') > -1,
            msg="No success for %s" % page
        )

    def file_mode_test(self, filename: str, mode: str):
        # Compare (eg) drwx???rw- to drwxr-xrw-
        result = self.container.exec_run("ls -ld %s" % filename).decode('utf-8')
        self.assertFalse(
            result.find("No such file or directory") > -1,
            msg="%s is missing" % filename
        )
        for char_count in range(0, len(mode)):
            self.assertTrue(
                mode[char_count] == '?' or (mode[char_count] == result[char_count]),
                msg="%s incorrect mode: %s" % (filename, result)
            )

    # <tests to run>

    def test_docker_logs(self):
        expected_log_lines = [
            "Loading php config",
            "Loading plugin /opt/configurability/goplugins/php.so"
        ]
        container_logs = self.container.logs().decode('utf-8')
        for expected_log_line in expected_log_lines:
            self.assertTrue(
                container_logs.find(expected_log_line) > -1,
                msg="Docker log line missing: %s from (%s)" % (expected_log_line, container_logs)
            )

    def test_apache_var_www_html(self):
        self.file_mode_test("/var/www/html", "drwxrwxrwx")

    def test_php_curl(self):
        self.check_success("curltest.php")

    def test_php_gd(self):
        self.check_success("gdtest.php")

    def test_php_gettext(self):
        self.check_success("gettexttest.php")

    def test_php_imagick(self):
        self.check_success("imagicktest.php")

    def test_php_imap(self):
        self.check_success("imaptest.php")

    def test_php_intl(self):
        self.check_success("intltest.php")

    def test_php_mbstring(self):
        self.check_success("mbstringtest.php")

    def test_php_mysql(self):
        self.check_success("mysqltest.php")

    def test_php_phpversion(self):
        self.check_success("phpversion.php")

    def test_php_soap(self):
        self.check_success("soaptest.php")

    def test_php_sqlite(self):
        self.check_success("sqlitetest.php")

    def test_php_xml(self):
        self.check_success("xmltest.php")

    def test_php_zip(self):
        self.check_success("ziptest.php")

    def test_php_info(self):
        # We need to set the desired headers, then get a new driver for this to work
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.X-Forwarded-For'] = "1.2.3.4"
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.X-Forwarded-Port'] = "99"
        driver = webdriver.PhantomJS()
        driver.get("http://%s:8080/phpinfo.php" % Test1and1ApacheImage.container_ip)
        self.assertTrue(
            driver.page_source.find("REMOTE_ADDR']</td><td class=\"v\">1.2.3.4") > -1,
            msg="phpinfo not showing REMOTE_ADDR=1.2.3.4 "
        )
        self.assertTrue(
            driver.page_source.find("SERVER_PORT']</td><td class=\"v\">99") > -1,
            msg="phpinfo not showing SERVER_PORT=99"
        )

    # </tests to run>

if __name__ == '__main__':
    unittest.main(verbosity=1)
