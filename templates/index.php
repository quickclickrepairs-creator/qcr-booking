<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class RepairShop extends CI_Controller {

  public function __construct() {
    parent::__construct();
    $this->load->model('Repair_model');
  }

  public function index() {
    // Display customer list
    $data['title'] = 'Repair Shop Software';
    $data['customers'] = $this->Repair_model->getCustomers();

    $this->load->view('index', $data);
  }
}
  <div class="back">
    <a href="/">← Back to Booking Page</a>
  </div>
</body>
</html>
