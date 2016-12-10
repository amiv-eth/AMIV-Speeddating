<?php

$handle = fopen("data/confirm.txt","a");
fwrite($handle,time()."\t$_GET[v]\t$_GET[mail]\n");

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>confirm</title>
	<meta name="generator" content="TextMate http://macromates.com/">
	<meta name="author" content="Stephan Müller">
	<!-- Date:  -->
</head>
<body>
<h1>OK</h1>
<p>Es hat funktioniert; neu laden bringt nichts ;-)</p>
</body>
</html>
