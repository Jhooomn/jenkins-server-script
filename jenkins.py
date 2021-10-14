import subprocess


def execute_bash_script(bash_command):
    output = subprocess.check_output(['bash', '-c', bash_command])
    if output is None or output == "":
        return ""
    return output


def update_package_list():
    execute_bash_script("sudo apt update")


def is_not_installed(script_output):
    return (script_output == "") or (script_output is None) or (script_output is False)


def install_java():
    update_package_list()
    execute_bash_script("sudo apt install default-jre -y")
    execute_bash_script("sudo apt install default-jdk -y")


def install_wget():
    update_package_list()
    execute_bash_script("sudo apt install wget -y")


def add_universe_repository():
    try:
        update_package_list()
        universe_repository_output = execute_bash_script("sudo add-apt-repository universe")
        common_universe_repository_messages_error = [
            "'universe' distribution component is already enabled for all sources"]
        if universe_repository_output in common_universe_repository_messages_error:
            print("It was already added universe repository")
        update_package_list()
    except Exception:
        print("There was an error with universe repository")


def install_jenkins():
    try:
        execute_bash_script("sudo apt-get install jenkins -y")
    except:
        print("There was an exception while Jenkins installation")


# validate if --> java is installed.
is_java_installed_output = execute_bash_script("which java")

if is_not_installed(is_java_installed_output):
    install_java()

# validate if --> wget is installed.
is_wget_installed_output = execute_bash_script("which wget")

if is_not_installed(is_wget_installed_output):
    install_wget()

# add gpg jenkins key
execute_bash_script("wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -.")

# add jenkins repository
execute_bash_script(
    "sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'.")

# add universe repository
add_universe_repository()

# install jenkins
install_jenkins()

# show secret jenkins-admin password
execute_bash_script("sudo less /var/lib/jenkins/secrets/initialAdminPassword")
