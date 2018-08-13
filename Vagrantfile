# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.ssh.forward_agent = true

  config.vm.provision "shell", inline: <<-SHELL
    yum update
    yum install -y @development mock fedpkg rpmdevtools copr-cli
    usermod -a -G mock vagrant
  SHELL
end
