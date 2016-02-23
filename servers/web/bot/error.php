<? 
function error($id)
{
header('Content-Type: text/html; charset=UTF-8');
switch ($id) {
    case 1:
        echo utf8_encode("error: contraseña incorrecta");
        break;
    case 2:
        echo utf8_encode("error: no se ingresó contraseña");
        break;
    case 3:
        echo utf8_encode("la sesión a expirado");
        break;
} 

?>
