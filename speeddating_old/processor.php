<?php

require_once('recaptchalib.php');
  $privatekey = "6LffosMSAAAAALnse60Cv831umvdWHOSQwEFvD0u";
  $resp = recaptcha_check_answer ($privatekey,
                                $_SERVER["REMOTE_ADDR"],
                                $_POST["recaptcha_challenge_field"],
                                $_POST["recaptcha_response_field"]);

  if (!$resp->is_valid) {
      include("captcha-fail.html");
  } else {

  
$where_form_is="http://".$_SERVER['SERVER_NAME'].strrev(strstr(strrev($_SERVER['PHP_SELF']),"/"));

$datum = $_POST['datum'];
$datum_output = "";

for($i=0; $i<10; $i++) {
	$datumId[$i] = 0;
}

$datum_output .= $_POST['datum0']." ";
$datum_output .= $_POST['datum1']." ";
$datum_output .= $_POST['datum2']." ";
$datum_output .= $_POST['datum3']." ";
$datum_output .= $_POST['datum4']." ";
$datum_output .= $_POST['datum5']." ";
$datum_output .= $_POST['datum6']." ";
$datum_output .= $_POST['datum7']." ";
$datum_output .= $_POST['datum8']." ";
$datum_output .= $_POST['datum9']." ";

if (isset($_POST['datum0'])) {$datumId[0] = 1;}
if (isset($_POST['datum1'])) {$datumId[1] = 1;}
if (isset($_POST['datum2'])) {$datumId[2] = 1;}
if (isset($_POST['datum3'])) {$datumId[3] = 1;}
if (isset($_POST['datum4'])) {$datumId[4] = 1;}
if (isset($_POST['datum5'])) {$datumId[5] = 1;}
if (isset($_POST['datum6'])) {$datumId[6] = 1;}
if (isset($_POST['datum7'])) {$datumId[7] = 1;}
if (isset($_POST['datum8'])) {$datumId[8] = 1;}
if (isset($_POST['datum9'])) {$datumId[9] = 1;}

//echo $datum_output;
  
  
// Connect
$link = mysql_connect('mysql.ee.ethz.ch', 'speeddating-ro', 'mi=oricu')
   OR die(mysql_error());

// Query
$query = sprintf("INSERT INTO `speeddating`.`2011` (
`Geschlecht` ,
`E-Mail` ,
`Studiengang` ,
`Semester`  ,
`Montag1`  ,
`Montag2`  ,
`Dienstag1`  ,
`Dienstag2`  ,
`Mittwoch1`  ,
`Mittwoch2`  ,
`Donnerstag1`  ,
`Donnerstag2`  ,
`Freitag1`  ,
`Freitag2`  ,
`WasErhoffstDuDir` ,
`WasIstDasPerfekteDate` ,
`SeitWannSingle` ,
`MeinungOnlineDating` ,
`BesterAnmachspruch` ,
`FrauenSind` ,
`MaennerSind` ,
`WasBietetEineBeziehung` ,
`WievieleDates` ,
`LaengsteBeziehung` ,
`WoKennenlernen` ,
`40JahreSingleWoKennenlernen` ,
`Obst`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');",
            mysql_real_escape_string($_POST['field_1']),
            mysql_real_escape_string($_POST['field_2']),
            mysql_real_escape_string($_POST['field_3']),
            mysql_real_escape_string($_POST['field_4']),
				mysql_real_escape_string($datumId[0]),
				mysql_real_escape_string($datumId[1]),
				mysql_real_escape_string($datumId[2]),
				mysql_real_escape_string($datumId[3]),
				mysql_real_escape_string($datumId[4]),
				mysql_real_escape_string($datumId[5]),
				mysql_real_escape_string($datumId[6]),
				mysql_real_escape_string($datumId[7]),
				mysql_real_escape_string($datumId[8]),
				mysql_real_escape_string($datumId[9]),
				mysql_real_escape_string($_POST['field_5']),
				mysql_real_escape_string($_POST['field_6']),
				mysql_real_escape_string($_POST['field_7']),
				mysql_real_escape_string($_POST['field_8']),
				mysql_real_escape_string($_POST['field_9']),
				mysql_real_escape_string($_POST['field_10']),
				mysql_real_escape_string($_POST['field_11']),
				mysql_real_escape_string($_POST['field_12']),
				mysql_real_escape_string($_POST['field_13']),
				mysql_real_escape_string($_POST['field_14']),
				mysql_real_escape_string($_POST['field_15']),
            mysql_real_escape_string($_POST['field_16']),
            mysql_real_escape_string($_POST['field_18']))
            ;

//echo $query;

mysql_query($query);

mail("speeddating@amiv.ethz.ch","Anmeldung fuers Speeddating - Formular","Form data:

Geschlecht *: " . $_POST['field_1'] . " 
E-Mail Adress *: " . $_POST['field_2'] . " 
Studiengang *: " . $_POST['field_3'] . " 
Semester: " . $_POST['field_4'] . " 
Datum: " . $datum_output . " 
Was erhoffst du dir vom Speed-Dating?: " . $_POST['field_5'] . " 
Was ist für dich das perfekte Date?: " . $_POST['field_6'] . " 
Seit wann bist du Single?: " . $_POST['field_7'] . " 
Wie stehst du zum Thema Online-Dating?: " . $_POST['field_8'] . " 
Dein bester Anmachspruch?: " . $_POST['field_9'] . " 
Frauen sind...: " . $_POST['field_10'] . " 
Männer sind…: " . $_POST['field_11'] . " 
Was bietet dir eine Beziehung, abgesehen vom Sex?: " . $_POST['field_12'] . " 
Wieviele Dates hattest du im letzten Jahr?: " . $_POST['field_13'] . " 
Meine längste Beziehung dauerte...: " . $_POST['field_14'] . " 
Wo lernst du (ausser beim Speeddating natuerlich) neue Leute kennen?: " . $_POST['field_15'] . " 
Stell dir vor, du bist 40 Jahre alt und Single. Wo würdest du dein Date kennenlernen?: " . $_POST['field_16'] . " 
Banane, Apfel, oder Birne? Warum?: " . $_POST['field_18'] . " 
");


include("confirm.html");

}

?>