<?php
$nick = $_POST['Nickname'];
$email = $_POST['Email'];
$nick = htmlspecialchars($nick);
$email = htmlspecialchars($email);
$nick = urldecode($nick);
$email = urldecode($email);
$nick = trim($nick);
$email = trim($email);
echo $nick;
echo "<br>";
echo $email;
if (mail(email, "Заявка с сайта", "ФИО:".$nick.". E-mail: ".$email ,"From: example2@mail.ru \r\n"))
 {     echo "сообщение успешно отправлено";
} else {
    echo "при отправке сообщения возникли ошибки";
}?>
