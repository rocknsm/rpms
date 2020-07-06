# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.ssh.forward_agent = true

#  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "8192"
    v.vmx["numvcpus"] = "6"
  end

  config.vm.provider "virtualbox" do |v|
    v.linked_clone = true
    v.memory = 8192
    v.cpus = 6
  end

  config.vm.provision "shell", inline: <<-SHELL
    yum update -y
    yum install -y epel-release
    yum install -y @development mock fedpkg rpmdevtools copr-cli \
      distribution-gpg-keys vim
    usermod -a -G mock vagrant
  SHELL
end
