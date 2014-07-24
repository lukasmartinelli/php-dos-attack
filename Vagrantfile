# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  #config.vm.define "lucid" do |lucid|
  #    lucid.vm.box_url = "http://files.vagrantup.com/lucid64.box"
  #    lucid.vm.box = "lucid64"
  #end

  config.vm.define "trusty" do |trusty|
      trusty.vm.box = "ubuntu/trusty64"
      trusty.vm.network "forwarded_port", guest: 80, host: 8080
      trusty.vm.synced_folder "server/", "/var/www/html"
  end

  config.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
  end
end
