# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.ssh.forward_agent = true

  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provider "vmware_desktop" do |v|
    v.vmx["memsize"] = "8192"
    v.vmx["numvcpus"] = "6"
  end

  config.vm.provision "shell", inline: <<-SHELL
    yum update
    yum install -y @development mock fedpkg rpmdevtools copr-cli
    usermod -a -G mock vagrant
  SHELL
end
