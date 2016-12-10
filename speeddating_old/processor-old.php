<?php

$where_form_is="http://".$_SERVER['SERVER_NAME'].strrev(strstr(strrev($_SERVER['PHP_SELF']),"/"));

// Connect
//$link = mysql_connect('mysql.ee.ethz.ch', 'speeddating-ro', 'c1cDLqx4nVWbS0ybg8Cq')
//   OR die(mysql_error());

// Query
//$query = sprintf("INSERT INTO '2011' VALUES ()",
//            mysql_real_escape_string($user),
//            mysql_real_escape_string($password));

$datum = $_POST['datum'];
$datum_output = "";
  if(empty($datum))
  {
    $datum_output = "Kein Termin gewaehlt";
  }
  else
  {
    $N = count($datum);
 
    for($i=0; $i < $N; $i++)
    {
      $datum_output .= $datum[$i] . " ";
    }
  }


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

?>
