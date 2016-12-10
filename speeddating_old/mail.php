<?php

session_start();

if (@$_GET['a']=='logout') {
	session_start();
	$_SESSION['loggedin'] = false;
	//session_destroy();
	header("location: mail.php?a=list");
	exit;
}

if (isset($_POST['password'])) {
	session_start();
	if (md5($_POST['password'])=='a5cc81ceb4385abad486af2943e572c7') {
		$_SESSION['loggedin'] = true;
	} else {
		$_SESSION['loggedin'] = false;
	}
	header("location: mail.php?a=list");
	exit;
}

if (@$_SESSION['loggedin']) {
	echo "<a href='mail.php?a=logout'>logout</a><br>";
} else {
	echo "<p><form action=\"mail.php\" method=\"post\" accept-charset=\"utf-8\">
		<label for=\"password\">Passwort</label> <input type=\"password\" name=\"password\" value=\"\" id=\"password\">
		<input type=\"submit\" value=\"Continue &rarr;\"></p>
	</form>";
	exit;
}


?><!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
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

//$anmeldungen = json_decode(file_get_contents("data/anmeldungen.json"),true);

//$personByMail = array();
//foreach ($anmeldungen as $person) {
//	$personByMail[trim($person['mail'])] = $person;
//}
////echo "<pre>"; print_r($personByMail); echo "</pre>\n";

$confirm = array();
$file = file("data/confirm.txt");
foreach ($file as $line) {
	$line = explode("\t",$line);
	$mail = trim($line[2]);
	$confirm[$mail] = $line[1];
}

$dates = array();
$currentDate = 'null';
$file = file("data/einteilung.txt");
foreach ($file as $line) {
	$line = explode(';',$line);
	if (count($line)<4) {
		echo implode(';',$line).'<br>';
		if (trim($line[0])=='') continue;
		$currentDate = trim($line[0]);
		continue;
	}
	$mail = trim($line[2]);
	$dates[$currentDate] []= $mail;
	//$person = $personByMail[$mail];
	//if ($currentDate!='free'&&!in_array($currentDate,$person['date'])) echo "$mail !!!<br>";
	$line[4] = (@$confirm[$mail]==null) ? ' no' : ' '.$confirm[$mail];
	echo implode(';',$line).'<br>';
}

$out = <<<EOF
Du hast dich im Verlauf der letzten Wochen für das Uni- und ETH-weite Speed-Dating angemeldet. Es freut uns zu sehen, dass unser Event auch nach vier Jahren immer noch bei so vielen Leuten auf Interesse stösst.

Leider müssen wir dir jedoch mitteilen, dass du wegen der grossen Nachfrage am diesjährigen Speed-Dating nicht dabei bist. Da sich jedoch jedes Jahr einzelne Teilnehmer abmelden oder ihre Anmeldung nicht bestätigen, gibt es jedoch die Möglichkeit kurzfristig einen Platz zu ergattern. Falls du immer noch Lust hast dabei zu sein, bitten wir dich deine Mails am Sonntag (Bestätigungs-Deadline) und im Verlauf der Woche ab und zu zu überprüfen.

Freundliche Grüsse
Dein Speed-Dating OK
EOF;

$in = <<<EOF
Du hast dich im Verlauf der letzten Wochen für das Uni- und ETH-weite Speed-Dating angemeldet. Es freut uns zu sehen, dass unser Event auch nach vier Jahren immer noch bei so vielen Leuten auf Interesse stösst. Aber jetzt zu den wichtigen Infos:

Es freut uns dir mitzuteilen, dass du am diesjährigen Speed-Dating dabei bist! Dein Termin  ist der DATE. (Die Termine am Montag und Dienstag wurden um 30min verschoben.)

Wir bitten dich jedoch noch bis am Sonntag um 12:00 Uhr deinen Termin via folgendem Link zu bestätigen. Nicht bestätigte Plätze werden nach diesem Termin an andere Personen weitergegeben. Alle andere wichtige Informationen zum Speed-Dating werden dir nach dem Bestätigungstermin noch separat per Mail verschickt.

Termin Bestätigen: CONFIRM
Termin Ablehnen: NONCONFIRM

Freundliche Grüsse
Dein Speed-Dating OK

PS: Wegen der grossen Anzahl angemeldeten Personen, können wir auch dieses Jahr wieder 10 Speed-Dating Termine organisieren. Leider fehlen uns jedoch einzelne Frauen um alle Speed-Datings vollständig auszulasten. Wenn ihr eine Kollegin oder Freundin kennt, die auch noch Lust hätte teilzunehmen, steht die Anmeldung für Frauen weiterhin offen. Verwendet dazu den direkten Link:

http://speeddating.ethz.ch/form.php

EOF;

$inOut = array();
$inOut['in'] = array();
$inOut['out'] = array();
$inOut['no'] = array();

foreach ($dates as $d=>$addr) {
	$date = 'error';
	if ($d!='free') {
		$d = explode('_',$d);
		$d[3] = substr_replace($d[3],':',2,0);
		$date = "$d[0].$d[1].$d[2], $d[3] Uhr";
	}
	foreach ($addr as $a) {
		$inLink = "http://speeddating.ethz.ch/confirm.php?v=in&mail=$a";
		$outLink = "http://speeddating.ethz.ch/confirm.php?v=out&mail=$a";
		if ($d=='free') {
			continue;
			$subject = "Speeddating";
			$text = $out;
		} else {
			$subject = "Speeddating: Termin bestätigen!";
			$text = $in;
		}
		$text = str_replace('DATE',$date,$text);
		$text = str_replace('NONCONFIRM',$outLink,$text);
		$text = str_replace('CONFIRM',$inLink,$text);
		//echo "<pre>"; print_r($text); echo "</pre>\n";
		//echo "$a\n";
		$cnf = @$confirm[$a];
		if ($cnf==null) $inOut['no'][] = $a;
		else $inOut[$cnf][] = $a;
		//mail($a,$subject,$text);
	}
}

foreach ($inOut as $k=>$v) {
	echo "<br>$k:<br><br>".implode(', ',$v)."<br>";
}
