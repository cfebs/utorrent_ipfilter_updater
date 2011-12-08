uTorrent ipfilter Updater
=========================

Provide a means to manage and update a ipfilter blocklist with minimal effort (no copy pasting)

Status
------

Still designing + planning, but given a list of url's to filters:

* request files from urls, download them
* combine in to one file in `.dat` format
* update `ipfilter.dat` on a Windows system


Based off [Transmission's](http://www.transmissionbt.com) methods after learning how it worked from the [source](https://trac.transmissionbt.com/browser/trunk/libtransmission/blocklist.c).
