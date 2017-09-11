<?php

$request = new HttpRequest();
$request->setUrl('http://127.0.0.1:5000/register');
$request->setMethod(HTTP_METH_POST);

$request->setHeaders(array(
  'postman-token' => 'db5ec391-2f12-bd7f-ae0e-44d5483bec3b',
  'cache-control' => 'no-cache',
  'content-type' => 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
));

$request->setBody('------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="username"

toto
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="email"

toto@gmail.com
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="password"

toto
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="confirm"

toto
------WebKitFormBoundary7MA4YWxkTrZu0gW--');

try {
  $response = $request->send();

  echo $response->getBody();
} catch (HttpException $ex) {
  echo $ex;
}