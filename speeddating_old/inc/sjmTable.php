<?php

// DEBUG: sql error messages propagate within log array
// DEBUG: if ($where) führt zu problemen bei 0!!!
// DEBUG: integer häufig als string.

// (c) 2008 - 2012 by stephan j. müller

class sjmTable {
	public $db;
	public $args;
	public $log = false; // array() to debug
	
	public function __construct($db,$table=false,$args=array()) {
		$this->db = $db;
		$args['table'] = $table;
		if (!isset($args['primary_key'])) $args['primary_key'] = 'id';
		$this->args = $args;
	}
	
	public function QueryExec($query) {
		$n = $this->db->exec($query); // affected rows
		if ($this->log!==false) $this->log($query);
		return $n;
	}
	public function QueryFetch($query) {
		$statem = $this->db->prepare($query);
		if ($this->log!==false) $this->log($query);
		if ($statem===false) return false;
		if (!$statem->execute()) return false;
		$data = $statem->fetchAll(PDO::FETCH_ASSOC);
		return $data;
	}
	
	public function insert($data,$args=array()) {
		$args = array_merge($this->args,$args);
		$query = 'INSERT INTO '.$args['table'];
		$query.= ' ('.implode(',',array_keys($data)).')';
		$query.= ' VALUES('.$this->SQLlist($data).');';
		$statem = $this->db->prepare($query);
		if ($this->log!==false) $this->log($query);
		if($statem===false) return false;
		if (!$statem->execute()) return false;
		return (int)$this->db->lastInsertId();
	}
	public function multiInsert(&$dataArray,$args=array()) {
		$args = array_merge($this->args,$args);
		if (!count($dataArray)) return true;
		$queries = array();
		foreach ($dataArray as $data) {
			$query = 'INSERT INTO '.$args['table'];
			$query.= ' ('.implode(',',array_keys($data)).')';
			$query.= ' VALUES('.$this->SQLlist($data).');';
			$queries []= $query;
		}
		$query = implode("\n",$queries);
		$n = $this->db->exec($query);
		if ($this->log!==false) $this->log($query);
		return true;
	}
	public function select($keys,$where=false,$args=array()) {
		$args = array_merge($this->args,$args);
		if (is_array($keys)) $keys = implode(',',$keys);
		$query = 'SELECT '.$keys.' FROM '.$args['table'];
		if ($where || $where===0) {
			if (is_array($where)) $where = $this->SQLeqexpr($where);
			elseif (is_integer($where)) $where = $this->args['primary_key'].'='.$where;
			$query.= ' WHERE '.$where;
		}
		if (isset($args['append'])) $query .= ' '.$args['append'];
		if (isset($args['order_by'])) {
			$query.= ' ORDER BY '.$args['order_by'];
		}
		if (isset($args['limit'])) {
			$query.= ' LIMIT '.$args['limit'];
			if (isset($args['offset'])) {
				$query.= ' OFFSET '.$args['offset'];
			}
		}
		return $this->QueryFetch($query.';');
	}
	public function update($where,$data,$args=array()) {
		$args = array_merge($this->args,$args);
		$query = 'UPDATE '.$args['table'];
		$query.= ' SET '.$this->SQLassign($data);
		if ($where || $where===0) {
			if (is_array($where)) $where = $this->SQLeqexpr($where);
			elseif (is_integer($where)) $where = $this->args['primary_key'].'='.$where;
			$query.= ' WHERE '.$where;
		}
		if (isset($args['append'])) $query .= ' '.$args['append'];
		if (isset($args['sql'])&&$args['sql']) return $query;
		$n = $this->db->exec($query.';'); // affected rows
		if ($this->log!==false) $this->log($query.';');
		return $n;
	}
	public function delete($where,$args=array()) {
		$args = array_merge($this->args,$args);
		$query = 'DELETE FROM '.$args['table'];
		if (!$where || is_string($where)) return 0; // prevent disasters
		if ($where || $where===0) {
			if (is_array($where)) $where = $this->SQLeqexpr($where);
			elseif (is_integer($where)) $where = $this->args['primary_key'].'='.$where;
			$query.= ' WHERE '.$where;
		}
		if (isset($args['append'])) $query .= ' '.$args['append'];
		$n = $this->db->exec($query.';'); // affected rows
		if ($this->log!==false) $this->log($query);
		return $n;
	}
	
	public function count($where,$args=array()) {
		$x = $this->select('count(*) AS c',$where,$args);
		if ($x===false) return false;
		return $x[0]['c'];
	}
	public function get($keys,$where,$args=array()) {
		$args['limit'] = 1;
		$x = $this->select($keys,$where,$args);
		if ($x===false || !count($x)) return false;
		return $x[0];
	}
	
	public function ArgSet($key,&$value) {
		$this->args[$key] = $value;
	}
	public function ArgUnset($key) {
		unset($this->args[$key]);
	}
	
	public function SQLlist($values) {
		foreach ($values as &$v) $v = $this->SQLquote($v);
		return implode(',',$values);
	}
	public function SQLassign($pairs) {
		foreach ($pairs as $k=>&$v) $v = $k.'='.$this->SQLquote($v);
		return implode(',',$pairs);
	}
	public function SQLeqexpr($pairs) {
		foreach ($pairs as $k=>&$v) {
			if (is_integer($k)) continue; // $v = $v;
			elseif (is_null($v)) $v = $k.' ISNULL';
			elseif (is_array($v)) $v = $k.' IN ('.$this->SQLlist($v).')';
			else $v = $k.'='.$this->SQLquote($v);
		}
		return implode(' AND ',$pairs);
	}
	public function SQLquote($v) {
		if (is_string($v)) return $this->db->quote($v);
		elseif (is_int($v)) return $v;
		elseif (is_null($v)) return 'NULL';
		else return $this->db->quote($v);
	}
	
	private function log($query) {
		$entry = $this->db->errorInfo();
		$entry []= $query;
		$this->log []= $entry;
	}
}


?>