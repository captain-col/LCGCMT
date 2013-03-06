#!/usr/bin/env python

import os, sys, time, string
import re
import cgi
import time
import MySQLdb
import lcg.msg

class confFill() :

  def __init__(self,lcgcmt,msgLevel) :
    self.msg = lcg.msg.msg(os.path.basename(sys.argv[0]), msgLevel)
    self.lcgcmt = lcgcmt
    self.cursor = None
    #form = cgi.FieldStorage()
        
  def dbFill(self) :
    pwdf = open('%s/private/lcgconf.pwd'%os.environ['HOME'])
    firstl = pwdf.readline().split()
    pwdf.close()
    host = firstl[0]
    port = int(firstl[1])
    user = firstl[2]
    pwd  = firstl[3]
    dbs   = firstl[4]
    db = MySQLdb.connect(host=host, port=port, user=user, passwd=pwd, db=dbs)
    self.cursor = MySQLdb.cursors.DictCursor(db)
    self.confFill()
    db.close()

  def confFill(self):

  #                   Structure of 'lcgcmt' dictionary
  #                   --------------------------------
  #
  # lcgcmt['general'] ---- ['name']       : e.g. LCG_xy
  #                        ['rel_date']   : unixtime value of the release date
  #                        ['motivation'] : blabla
  #                             --- for any new platform, add: ---
  #       ['plat_def'] --- [platf name]['os']
  #                                    ['arch']
  #                                    ['comp']
  #                                    ['dbg']
  #
  #       ['platforms'] -- list of supported platforms names
  #
  #             --- for ALL packages included in the configuration ---
  #
  #       ['pkg'][pkg name]['version'][vers_name]
  #                                   --- if version is new, add: ---
  #                                              ['platform'][plat]['src_tarball']
  #                                                                ['bin_tarball']
  #                                                                ['afs_relpath']
  #                                              ['dep'] list of pkg names 
  #
  #                        --- if package is new, add: ---
  #                        ['contacts'][name1] = email1 dict of contact persons
  #                                    [name2] = email2
  #                        ['homepage']
  #                        ['short_descrip']
  #                        ['long_descrip']
  #                        ['category']
  #                        ['language']
  #
  #                        ['is_project'] : 1 if pakg is project else 0
  #                             --- if (is_project == 1) add: ---
  #                        ['proj_..1']
  #                            ...
  #                        ['proj_..N']

  #                             --- if (is_project == 0) add: ---
  #                        ['exts_..1']
  #                            ...
  #                        ['exts_..N']


  ### Declare NEW CONFIGURATION

    self.cursor.execute("SELECT conf_name \
                    FROM configurations \
                    WHERE conf_name='"+self.lcgcmt['general']['name']+"'")
    result = self.cursor.fetchall()
    confname = ''
    for record in result:
      confname = str(record['conf_name'])
    if (confname == ''):
      sql = "INSERT INTO configurations (conf_name, release_date, motivation) VALUES(%s, %s, %s)"
      self.cursor.execute(sql, (self.lcgcmt['general']['name'], self.lcgcmt['general']['rel_date'], self.lcgcmt['general']['motivation']))
      self.msg.info("[%s] configuration added to the database" % self.lcgcmt['general']['name'] )
    else:
      self.msg.warning("[%s] configuration already known by the database" % self.lcgcmt['general']['name'])

    # get id of new configuration to use later
    self.cursor.execute("SELECT conf_id \
                    FROM configurations \
                    WHERE conf_name='"+self.lcgcmt['general']['name']+"'")
    result = self.cursor.fetchall()
    for record in result:
      new_cfg_id = record['conf_id']

  ### Declare any NEW PLATFORM

    # get all known platforms
    self.cursor.execute("SELECT name \
                    FROM platforms")
    result = self.cursor.fetchall()
    kplatforms = []
    for record in result:
      kplatforms.append(str(record['name']))

    # check if all platforms supported by the new configuration are known
    plist = self.lcgcmt['platforms']
    for plat in plist:
      if (plat not in kplatforms):
        ### Declare the NEW PLATFORM
        if (not(self.lcgcmt['plat_def'][plat].has_key('dbg'))):
          self.lcgcmt['plat_def'][plat]['dbg'] = '' 
        sql = "INSERT INTO platforms (name, os, arch, comp, dbg) VALUES(%s, %s, %s,%s, %s)"
        self.cursor.execute(sql, (plat, self.lcgcmt['plat_def'][plat]['os'], self.lcgcmt['plat_def'][plat]['arch'], self.lcgcmt['plat_def'][plat]['comp'], self.lcgcmt['plat_def'][plat]['dbg']))
        self.msg.info("[%s] platform added to the database" % plat)
    # get all (updated) platforms by name and id
    self.cursor.execute("SELECT name, plat_id \
                    FROM platforms")
    result = self.cursor.fetchall()
    dplatid = {}
    for record in result:
      dplatid[str(record['name'])] = record['plat_id']

    # check if the database knows which platforms are supported by the new config
    self.cursor.execute("SELECT platforms.name \
                    FROM platforms, conf_plat \
                    WHERE conf_plat.conf_id='"+str(new_cfg_id)+"' AND \
                          conf_plat.plat_id=platforms.plat_id")
    result = self.cursor.fetchall()
    configplats = []
    for record in result:
      configplats.append(str(record['name']))

    for plat in plist:
      if (plat not in configplats):
        ### Tell the db this platform is supported by the new config
        sql = "INSERT INTO conf_plat (conf_id, plat_id) VALUES(%s, %s)"
        self.cursor.execute(sql, (new_cfg_id, dplatid[plat]))
        self.msg.info("[%s] support of platform added to the database" % plat )

    ### Declare any PACKAGE unknown to the database

    # First get all known packages names
    self.cursor.execute("SELECT pkg_name \
                    FROM packages")
    result = self.cursor.fetchall()
    kpackages = []
    for record in result:
      kpackages.append(str(record['pkg_name']))

    # Check if the new configuration packages are already known
    pklist = self.lcgcmt['pkg'].keys()
    for pk in pklist:
      if (pk not in kpackages):
        ### Declare the NEW PACKAGE
        sql = "INSERT INTO packages (pkg_name, is_project, homepage, short_descrip, long_descrip, category, language) VALUES(%s, %s, %s, %s, %s, %s, %s)"

        self.cursor.execute(sql, (pk, self.lcgcmt['pkg'][pk]['is_project'], self.lcgcmt['pkg'][pk]['homepage'], self.lcgcmt['pkg'][pk]['short_descrip'], self.lcgcmt['pkg'][pk]['long_descrip'], self.lcgcmt['pkg'][pk]['category'], self.lcgcmt['pkg'][pk]['language']))

        # Get the package id
        self.cursor.execute("SELECT pkg_name, pkg_id \
                        FROM packages WHERE pkg_name='"+pk+"'")
        result = self.cursor.fetchall()
        for record in result:
          thispkgid = record['pkg_id']
        # Declare its CONTACT persons
        for cont in (self.lcgcmt['pkg'][pk]['contact']).keys():
          ### Check if contact is already known
          self.cursor.execute("SELECT contact_id \
                               FROM contacts \
                               WHERE LOWER(name)='"+cont.lower()+"'")
          result = self.cursor.fetchall()
          cont_id = 0
          for record in result:
            cont_id = record['contact_id']
          if (cont_id == 0):
            sql = "INSERT INTO contacts (name, email) VALUES(%s, %s)"
            self.cursor.execute(sql, (cont, self.lcgcmt['pkg'][pk]['contact'][cont]))
            self.msg.info("[%s] contact added to the database" % self.lcgcmt['pkg'][pk]['contact'][cont] )

            # get id of new contact to use later
            self.cursor.execute("SELECT contact_id \
                                 FROM contacts \
                                 WHERE name='"+cont+"'")
            result = self.cursor.fetchall()
            for record in result:
              cont_id = record['contact_id']

          sql = "INSERT INTO pkg_contact (pkg_id, contact_id) VALUES(%s, %s)"
          self.cursor.execute(sql, (thispkgid, cont_id))
        self.msg.info("[%s] package added to the database" % pk)

    # Now all involved packages are known to the db, let's get their id
    self.cursor.execute("SELECT pkg_name, pkg_id \
                    FROM packages")
    result = self.cursor.fetchall()
    dpkgid = {}
    for record in result:
      dpkgid[str(record['pkg_name'])] = record['pkg_id']

    # first get the version(s) of the packages in this configuration
    # for every package included in this configuration
    for pk in pklist:
      # get the version(s) of this pkg in this config
      versions = self.lcgcmt['pkg'][pk]['version'].keys()

      max_plat = 0
      common_version = ''
      for v in versions:
        if (len(self.lcgcmt['pkg'][pk]['version'][v]['platform'].keys()) > max_plat):
          common_version = v

      for v in versions:
        # check if this version is already known by the db
        is_new_version = 0
        self.cursor.execute("SELECT pkg_version.pkg_version_id \
                        FROM packages, pkg_version \
                        WHERE pkg_version.vers_name='"+v+"' AND \
                              pkg_version.pkg_id="+str(dpkgid[pk]))
        result = self.cursor.fetchall()
        pkgvid = -1
        for record in result:
          pkgvid = record['pkg_version_id']

        # if unknown, declare the NEW VERSION of this package
        if (pkgvid == -1):
          is_new_version = 1
          if (not(self.lcgcmt['pkg'][pk].has_key('motivation'))):
            self.lcgcmt['pkg'][pk]['motivation'] = ''       
          sql = "INSERT INTO pkg_version (pkg_id, vers_name, motivation, afs_relpath) VALUES(%s, %s, %s, %s)"
          self.cursor.execute(sql, (dpkgid[pk], v, self.lcgcmt['pkg'][pk]['motivation'], self.lcgcmt['pkg'][pk]['afs_relpath']))
          self.msg.info("[%s] version %s of added to the database" % (pk,v))

          # and get its pkg_version_id
          self.cursor.execute("SELECT pkg_version.pkg_version_id \
                          FROM packages, pkg_version \
                          WHERE pkg_version.vers_name='"+v+"' AND \
                                pkg_version.pkg_id="+str(dpkgid[pk]))
          result = self.cursor.fetchall()
          pkgvid = -1
          for record in result:
            pkgvid = record['pkg_version_id']

        this_vers_plist = self.lcgcmt['pkg'][pk]['version'][v]['platform'].keys()
        # for every platform this package version is used on in this config
        for plat in this_vers_plist:
          # if it's a new version, insert references to tarballs
          if (is_new_version == 1):
            sql = "INSERT INTO pkg_plat (pkg_version_id, plat_id, bin_tarball, src_tarball) VALUES(%s, %s, %s, %s)"
            self.cursor.execute(sql, (pkgvid, dplatid[plat], self.lcgcmt['pkg'][pk]['version'][v]['platform'][plat]['bin_tarball'], self.lcgcmt['pkg'][pk]['version'][v]['platform'][plat]['src_tarball']))
          # if this version is not the one used on the majority of platforms
          if (v != common_version):
            # tell that in the new config, this pkg version is used for this plat
            sql = "INSERT INTO pkg_plat_conf (pkg_version_id, plat_id, conf_id) VALUES(%s, %s, %s)"
            self.cursor.execute(sql, (pkgvid, dplatid[plat], new_cfg_id))
        # end loop on platforms

        # tell the database which packages this version depends on
        deplist = self.lcgcmt['pkg'][pk]['version'][v]['dep']

        for pk in deplist:
          sql = "INSERT INTO pkg_dep (pkg_version_id, dep_on_pkg) VALUES(%s, %s)"
          self.cursor.execute(sql, (pkgvid, dpkgid[pk]))
      # end loop on versions

      # tell the db which version of this pkg is the common one in the new conf
      self.cursor.execute("SELECT pkg_version.pkg_version_id \
                      FROM packages, pkg_version \
                      WHERE pkg_version.vers_name='"+common_version+"' AND \
                            pkg_version.pkg_id="+str(dpkgid[pk]))
      result = self.cursor.fetchall()
      pkgvid = -1
      for record in result:
        pkgvid = record['pkg_version_id']
      sql = "INSERT INTO pkg_conf (pkg_version_id, conf_id) VALUES(%s, %s)"
      self.cursor.execute(sql, (pkgvid, new_cfg_id))

    # end loop on pk

  #                 ------------------------------------------

if __name__ == "__main__":

    pkg_descr = {}

    form = cgi.FieldStorage()

    db = MySQLdb.connect("localhost", "root", "root4spi", "test")

    cursor = MySQLdb.cursors.DictCursor(db)

    lcgcmt             = {}
    lcgcmt['general']  = {}
    lcgcmt['plat_def'] = {}
    lcgcmt['pkg']      = {}

    confFill()
    db.close()

