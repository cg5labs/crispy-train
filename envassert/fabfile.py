# https://pypi.python.org/pypi/envassert
# Test your servers environments by using fabric.

from fabric.api import env, task
from envassert import file, process, package, user, group, port, cron, detect, service, filesystem

env.use_ssh_config = True

@task
def check():
    env.platform_family = detect.detect()

    assert file.exists("/etc/hosts")
    assert file.is_file("/etc/hosts")
    assert file.is_dir("/tmp/")
    assert file.dir_exists("/tmp/")
    assert file.has_line("/etc/passwd", "sshd")
    assert file.owner_is("/bin/sh", "root")
    assert file.group_is("/bin/sh", "root")
    assert file.mode_is("/bin/sh", "777")

    if env.platform_family == "freebsd":
        assert file.is_link("/compat")
    else:
        assert file.is_link("/usr/tmp")

    # this check needs to run as root
    #assert package.installed("wget.x86_64")

    assert user.exists("sshd")
    # this check doesn't work with systemd
    #assert service.is_enabled("sshd")
    assert user.is_belonging_group("ec2-user", "adm")
    # module error on group.exist
    #assert group.exists("adm")

    assert port.is_listening(22)
    #assert port.is_listening(80, "tcp")

    assert process.is_up("http") is False

    assert filesystem.is_type('xfs', '/')
