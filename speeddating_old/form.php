<?php


// require_once "inc/sjmFields.php";
require_once "inc/SJMForm.php";

$form = <<<EOF
radio sex("Geschlecht *"){ option f("Weiblich"); option m("Männlich"); };
text mail("E-Mail Adresse *");
text studiengang("Studiengang *");
text semester("Semester");
text age("Alter");
checkbox date("Speed-Dating Termin") {
	option 23_5_2014_1830("Donnerstag 28. April 18:30, Altersgruppe unter 22");
	option 23_5_2014_2300("Donnerstag 28. April 20:30, Altersgruppe 21-25");
	option 24_5_2014_1830("Freitag 29. April 18:30, Altersgruppe 21-25");
	option 24_5_2014_2300("Freitag 29. April 20:30, Altersgruppe ab 24");
};
EOF;

$questions = <<<EOF
textarea aspirations("Was erhoffst du dir vom Speed-Dating?");
textarea perfectdate("Was ist für dich das perfekte Date?");
text singlesince("Seit wann bist du Single?");
textarea onlinedating("Wie stehst du zum Thema Online-Dating?");
textarea pickupline("Dein bester Anmachspruch?");
textarea women("Frauen sind…");
textarea men("Männer sind…");
textarea vorteile("Was bietet dir eine Beziehung, abgesehen vom Sex?");
text datesprojahr("Wieviele Dates hattest du im letzten Jahr?");
text beziehungsdauer("Meine längste Beziehung dauerte…");
textarea kennenlernen("Wo lernst du (ausser beim Speeddating natuerlich) neue Leute kennen?");
textarea single40("Stell dir vor, du bist 40 Jahre alt und Single. Wo würdest du dein Date kennenlernen?");
textarea fruit("Banane, Apfel, oder Birne? Warum?");
EOF;

$fFields = new SJMForm($form);
$fFields->set($_POST);

$qFields = new SJMForm($questions);
$qFields->set($_POST);

// sent by mail when submitting form
$confirmation = <<<EOF
Deine Anmeldung ist bei uns eingetroffen und wir werden uns Mitte April bei dir melden.

Freundliche Grüsse
Das Speed-Dating Team
EOF;

if (isset($_POST['mail']) && $_POST['mail']) {
	// TODO: verification
	$valid = true;
	$data = $fFields->preprocess($_POST);
	$data['time'] = time();
	$data['ip'] = $_SERVER['REMOTE_ADDR'];
	$data['questions'] = $qFields->preprocess($_POST);
	$string = base64_encode(serialize($data))."\n";
	if ($valid) {
		file_put_contents("data/anmeldungen.txt", $string, FILE_APPEND | LOCK_EX);
		mail($_POST['mail'],"Anmeldung fuers Speeddating",$confirmation);
		include("confirm.html");
		exit;
	} else {
		// TODO: display error
		// form will be prefilled with previous content
	}
}

if (@$_GET['a']=='list') {
	session_start();
	if (@$_SESSION['loggedin']) {
		echo "<a href='form.php?a=logout'>logout</a><br>";
		$anmeldungen = file("data/anmeldungen.txt");
		foreach ($anmeldungen as $anmeldung) {
			$data = unserialize(base64_decode($anmeldung));
			$text = $data['questions']['aspirations'];
			if (strpos($text,'<a href=')!==false) continue;
			if (strpos($text,'http://')!==false) continue;
			if (strpos($data['mail'],'@')===false) continue;
			echo '<pre>'; print_r( $data ); echo '</pre>';
		}
		exit;
	} else {
		echo "<p><form action=\"form.php\" method=\"post\" accept-charset=\"utf-8\">
			<label for=\"password\">Passwort</label> <input type=\"password\" name=\"password\" value=\"\" id=\"password\">
			<input type=\"submit\" value=\"Continue &rarr;\"></p>
		</form>";
		exit;
	}
}

if (@$_GET['a']=='logout') {
	session_start();
	$_SESSION['loggedin'] = false;
	//session_destroy();
	header("location: form.php?a=list");
	exit;
}

if (isset($_POST['password'])) {
	session_start();
	$passwords = array('a5cc81ceb4385abad486af2943e572c7', '54fafccfbd2abfa84f077bd5f08ff1e8', '995f5bf580373d9bb5a71e3d4cbdd456');
	if (in_array(md5($_POST['password']), $passwords)) {
		$_SESSION['loggedin'] = true;
	} else {
		$_SESSION['loggedin'] = false;
	}
	header("location: form.php?a=list");
	exit;
}


//$foo->set($foo->get());

//echo '<form action="form.php" method="GET" accept-charset="utf-8">'."\n";
//echo $foo;
//echo '<p><input type="submit" value="Anmelden"></p></form>'."\n";
//
//echo '<pre>'; print_r($foo->get()); echo '</pre>';
//
//echo '<pre>'; print_r($_SERVER); echo '</pre>';
//
//echo '<pre>'; print_r($foo->filter($_GET)); echo '</pre>';
//
//echo '<pre>'; print_r($foo->elements); echo '</pre>';

//return;

?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
	<html>
	<head>
<title>

			speeddating :: an der ETH &amp; Uni Z&uuml;rich
</title>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8"><link href="style.css" rel="stylesheet" type="text/css">
<style type="text/css">

			@import url("screen.css") screen;

		</style>
	</head>

	<body>

	<div id="content-wrapper">




		<div id="formHeader-blub">
				<h2 class="formInfo">Speed Dating Fragebogen</h2>
				<p class="formInfo">
					Wir freuen uns, dass du an unserem Speed-Dating teilnehmen möchtest. Hier noch ein paar Informationen zum Fragebogen:
				</p>
				<ul>
					<li>Mit einem <strong>Sternchen (*) markierte Fragen sind obligatorisch</strong> und müssen beantwortet werden.</li>
					<li>Fragen die kein Sternchen haben sind freiwillig und müssen nicht unbedingt beantwortet werden.</li>
					<li>Je mehr Termine du angibst, desto höher sind deine Chancen dabei zu sein.</li>
					<li>Sämtliche Angaben sind sind zur internen Verwendung und werden nicht veröffentlicht. </li>
				</ul>
				<p class="formInfo">
					Viel Spass beim ausfüllen und falls du Fragen hast, schreib einfach eine Mail an speeddating@amiv.ethz.ch. <br><br>
					
					Dein Speed-Dating Team
				</p>
		</div>


		<BR/><!-- begin form -->

		<form method=post enctype=multipart/form-data action=form.php onSubmit="return validatePage2();" name=mainFormName>	

<ul class=mainForm id="mainForm_1">

				<li>
<?php echo $fFields.$qFields; ?>
				</li>
				
				
				<li class="mainForm">
					<input id="saveForm" class="mainForm" type="submit" value="Anmelden" />
				</li>

	  </form>
			<!-- end of form -->
		<!-- close the display stuff for this page -->
		</ul></div>

	</body>
	</html>
