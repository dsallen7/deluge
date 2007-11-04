#
# pluginmanager.py
#
# Copyright (C) 2007 Andrew Resch ('andar') <andrewresch@gmail.com>
# 
# Deluge is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.

"""PluginManager for Core"""

import deluge.pluginmanagerbase
from deluge.log import LOG as log

class PluginManager(deluge.pluginmanagerbase.PluginManagerBase):
    """PluginManager handles the loading of plugins and provides plugins with
    functions to access parts of the core."""
    
    def __init__(self, core):
        self.core = core
        # Set up the hooks dictionary
        self.hooks = {
            "post_torrent_add": [],
            "post_torrent_remove": []
        }
        
        self.status_fields = {}
        
        # Call the PluginManagerBase constructor
        deluge.pluginmanagerbase.PluginManagerBase.__init__(
            self, "core.conf", "deluge.plugin.core")

    def get_core(self):
        """Returns a reference to the core"""
        return self.core
        
    def register_status_field(self, field, function):
        """Register a new status field.  This can be used in the same way the
        client requests other status information from core."""
        log.debug("Registering status field %s with PluginManager", field)
        self.status_fields[field] = function
    
    def deregister_status_field(self, field):
        """Deregisters a status field"""
        log.debug("Deregistering status field %s with PluginManager", field)
        try:
            del self.status_fields[field]
        except:
            log.warning("Unable to deregister status field %s", field)
            
    def get_status(self, torrent_id, fields):
        """Return the value of status fields for the selected torrent_id."""
        status = {}
        for field in fields:
            try:
                status[field] = self.status_fields[field](torrent_id)
            except KeyError:
                log.warning("Status field %s is not registered with the\
                    PluginManager.", field)
        return status
        
    def register_hook(self, hook, function):
        """Register a hook function with the plugin manager"""
        try:
            self.hooks[hook].append(function)
        except KeyError:
            log.warning("Plugin attempting to register invalid hook.")
    
    def deregister_hook(self, hook, function):
        """Deregisters a hook function"""
        try:
            self.hooks[hook].remove(function)
        except:
            log.warning("Unable to deregister hook %s", hook)
            
    def run_post_torrent_add(self, torrent_id):
        """This hook is run after a torrent has been added to the session."""
        log.debug("run_post_torrent_add")
        for function in self.hooks["post_torrent_add"]:
            function(torrent_id)
            
    def run_post_torrent_remove(self, torrent_id):
        """This hook is run after a torrent has been removed from the session.
        """
        log.debug("run_post_torrent_remove")
        for function in self.hooks["post_torrent_remove"]:
            function(torrent_id)
   
