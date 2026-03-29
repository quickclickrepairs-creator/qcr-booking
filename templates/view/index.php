<?php
defined('BASEPATH') OR exit('No direct script access allowed');

$this->load->view('header');
?>

<h1>Customers</h1>

<table border="1">
  <tr>
    <th>Customer ID</th>
    <th>Name</th>
    <th>Email</th>
  </tr>

  <?php foreach ($customers as $customer) : ?>
  <tr>
    <td><?php echo $customer['CustomerID']; ?></td>
    <td><?php echo $customer['FirstName'] . ' ' . $customer['LastName']; ?></td>
    <td><?php echo $customer['EmailAddress']; ?></td>
  </tr>
  <?php endforeach; ?>
</table>

<?php
$this->load->view('footer');
?>
