class Repair_model extends CI_Model {

  public function __construct() {
    parent::__construct();
  }

  public function getCustomers() {
    $query = $this->db->get('customers');
    return $query->result_array();
  }
}
