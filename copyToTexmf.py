#!/usr/bin/python

# A python script to copy the files to a texmf directory.
# WARNING! this will remove any extra files in the base directories.

import os;
import sys;
import shutil;

def get_default_texmf_path():
	if sys.platform == "darwin":
		return os.path.join( os.path.expanduser( "~" ), "Library", "texmf" );
	else:
		return os.path.join( os.path.expanduser( "~" ), "texmf" );
# fed get_default_texmf_path()


def ensure_texmf_tree( basepath, mode = 0755 ):
	paths = [ basepath, os.path.join( basepath, "tex" ), \
		os.path.join( basepath, "tex", "latex" ), \
		os.path.join( basepath, "tex", "plain" ), \
		os.path.join( basepath, "doc" ), \
		os.path.join( basepath, "bibtex" ), \
		os.path.join( basepath, "bibtex", "bst" ) ];

	for pth in paths:
		if not os.path.isdir( pth ):
			os.makedirs( pth, mode );

	return;
#fed ensure_texmf_tree( basepath, mode = 0755 )

def rm( pth ):
	if os.path.isdir( pth ):
		for root, dirs, files in os.walk( pth ):
			for d in dirs:
				rm( os.path.join( pth, d ) );
				os.rmdir( os.path.join( pth, d ) );
			for f in files:
				os.remove( os.path.join( pth, f ) );
	return;
#fed rmr( pth )

def setup( texmf ):
	scriptdir = os.path.dirname( os.path.realpath( __file__ ) );
	output = [];

	cvbib = {};
	cvbib[ "src_dir" ] = os.path.join( scriptdir, "cvbib" );
	cvbib[ "dst_dir" ] = os.path.join( texmf, "tex", "latex", "cvbib" );
	cvbib[ "dirs" ] = [];
	cvbib[ "files" ] = [ "cvbib.sty" ];
	output.append( cvbib );

	return output;

if __name__ == "__main__":
	texmf_base = get_default_texmf_path();
	ensure_texmf_tree( texmf_base );
	packages = setup( texmf_base );
	for package in packages:
		if os.path.isdir( package[ "dst_dir" ] ):
			rm( package[ "dst_dir" ] );
		else:
			os.path.mkdir( package[ "dst_dir" ] );

		for d in package[ "dirs" ]:
			os.math.mkdir( d );

		for f in package[ "files" ]:
			shutil.copy( os.path.join( package[ "src_dir" ], f ), \
				os.path.join( package[ "dst_dir" ], f ) );



	