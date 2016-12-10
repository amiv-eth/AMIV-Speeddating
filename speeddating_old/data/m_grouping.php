<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title></title>
	<meta name="generator" content="TextMate http://macromates.com/">
	<meta name="author" content="Stephan Müller">
	<!-- Date:  -->
</head>
<body>

<?php

$people = array();

$anmeldungen = file("anmeldungen.txt");
foreach ($anmeldungen as $anmeldung) {
	$data = unserialize(base64_decode($anmeldung));
	$text = $data['questions']['aspirations'];
	if (strpos($text,'<a href=')!==false) continue;
	if (strpos($text,'http://')!==false) continue;
	if (strpos($data['mail'],'@')===false) continue;
	$data['date'] = explode(',',$data['date']);
	$people []= $data;
	//echo '<pre>'; print_r( $data ); echo '</pre>';
}

$people = array_filter($people,function($p){return $p['sex']=='m';});
$ids = array_keys($people);

//echo "<pre>"; print_r($people); echo "</pre>\n";

$dates = array('20_5_2014_1830', '20_5_2014_2300', '21_5_2014_1830', '21_5_2014_2300', '22_5_2014_1830', '22_5_2014_2300', '23_5_2014_1830', '23_5_2014_2300', '24_5_2014_1830', '24_5_2014_2300');

function choose($array,$n) {
	$tuples = array();
	if ($n==1) {
		foreach ($array as $i) {
			$tuples []= array($i);
		}
	} else {
		for ($i=0; $i < count($array)-1; $i++) { 
			$reduced = $array;
			$reduced = array_splice($reduced,$i);
			$element = array_shift($reduced); 
			$sub = choose($reduced,$n-1);
			foreach ($sub as $s) {
				array_unshift($s,$element);
				$tuples []= $s;
			}
		}
	}
	return $tuples;
}

if (false) { // combinations
	$dcombs = array();
	foreach (choose($dates,3) as $dcomb) {
		$remaining = $people;
		$dates = array();
		foreach ($dcomb as $d) {
			$nRemaining = count($remaining);
			$remaining = array_filter($remaining,function($p){global $d; return in_array($d,$p['date'])==false;});
			$dates[$d] = $nRemaining - count($remaining);
		}
		$dcombs []= array('dates'=>$dates, 'remaining'=>count($remaining));
	}

	foreach ($dcombs as $dcomb) {
		if ($dcomb['remaining']<=5) {
			echo "<pre>"; print_r($dcomb); echo "</pre>\n";
		}
	}
}

if (true) { // date table
	echo '<table border="1" cellspacing="5" cellpadding="5">';
	echo '<tr><th>mail</th><th>Age</th>';
	foreach ($dates as $d) {
		echo "<th>$d</th>";
	}
	echo '</tr>';

	foreach ($people as $p) {
		echo "<tr><td>$p[mail]</td>";
 		echo "<td>$p[age]</td>";
		foreach ($dates as $d) {
			if (in_array($d,$p['date'])) {
				echo "<td bgcolor='green'></td>";
			} else {
				echo "<td></td>";
			}
		}
		echo '</tr>';
	}

	echo '</table>';
}

if (false) {
	echo "<pre>"; print_r(count($people)); echo "</pre>\n";
	
	$dates = array_combine($dates,array_fill(0,count($dates),0));
	foreach ($people as $p) {
		foreach ($p['date'] as $d) {
			$dates[$d] += 1;
		}
	}

	echo "<pre>"; print_r($dates); echo "</pre>\n";
}


?>

</body>
</html>
