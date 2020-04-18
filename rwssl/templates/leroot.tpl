###############################################################################
# DO NOT EDIT OR REMOVE THIS FILE.
#
# This file rewrites ACME root in order to prevent issues during ACME challenge
# verification & later in renewal process. HTACCESS rules may interfere with
# ACME requests and may result in renewal failure. This conf file prevents that.
###############################################################################

location ^~ /.well-known/acme-challenge/ {
    default_type "text/plain";
    rewrite /.well-known/acme-challenge/(.*) /$1 break;
    root /var/.rwssl/.well-known/acme-challenge/;
}