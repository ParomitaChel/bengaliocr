<?php
//get data from form  

$name = $_POST['name'];
$email= $_POST['email address'];
$number= $_POST['mobile'];
$message= $_POST['message'];

$to = "bengaliocrmcacu22@rediffmail.com";

$subject = "Mail From BengaliOCR";
$txt ="Name = ". $name . "\r\n  Email = " . $email . "\r\n Mobile number =" . $number  "\r\n Message =" . $message;
$headers = "From: noreply@bengaliocrmcacu22.com" . "\r\n" .
#"CC: somebodyelse@example.com";
if($email!=NULL){
    mail($to,$subject,$txt,$headers);
}
//redirect
header("Location:thankyou.html");
?>