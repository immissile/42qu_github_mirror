<?php
/**
 * PHP handler for jWYSIWYG file uploader.
 *
 * By Alec Gorge <alecgorge@gmail.com>
 */

// an array of file extensions to accept
$accepted_extensions = array(
	"png", "jpg", "gif"
);

// http://your-web-site.domain/base/url
$base_url = '/uploads';

// the root path of the upload directory on the server
$uploads_dir = realpath("./uploads");

// the root path that the files are available from the webserver
// YOU WILL NEED TO CHANGE THIS
$uploads_access_dir = "/path/to/jwysiwyg/plugins/fileManager/handlers/PHP/uploads/";

$capabilities = array(
	"move" => true,
	"rename" => true,
	"remove" => true,
	"mkdir" => true,
	"upload" => true
);