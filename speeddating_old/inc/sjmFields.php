<?php 

/*
$foo = new sjmFields;

$in = file_get_contents('fields.txt');

$foo->compile($in);
$foo->set($_POST);

echo '<form action="sjmFields.php" method="post" accept-charset="utf-8">'."\n";
echo $foo;
echo '<p><input type="submit" value="Anmelden"></p></form>'."\n";

echo '<pre>'; print_r($foo->filter($_POST)); echo '</pre>';

echo '<pre>'; print_r($foo->elements); echo '</pre>';
*/

// (c) 2008 by stephan j. müller

// TODO: escape

// checkbox and radio fields only return predefined values (get_) or ''

class sjmFields {
	/*
	# $elements:
	array of elements
	# element:
	type:string
	args:array
	content:array of elements
	*/
	
	public $elements = array();
	
	public function compile($in) {
		// expression: type name(args) {content};
		//$in = str_replace('\\"','&#34;',$in);
		$expr = '/(\w+)\s+(\w+)\s*\((.*?)\)\s*(\{(.*?)\}\s*)?;/s';
		preg_replace_callback($expr,array($this,'compile_expression'),$in);
		
	}
	public function __toString() {
		$out = '';
		foreach ($this->elements as $e) {
			$method = 'render_'.$e['type'];
			if(!method_exists($this,$method)) continue;
			$out .= $this->$method($e);
		}
		return $out;
	}
	public function clear() { $this->elements = array(); }
	public function set($data,$field=false) {
		foreach ($this->elements as &$e) {
			$method = 'set_'.$e['type'];
			if(!method_exists($this,$method)) continue;
			if(!array_key_exists($e['name'],$data)) continue; // dont erase if no data
			if(!$field || $field==$e['name']) $this->$method($e,$data);
		}
	}
	public function get($data=array()) {
		foreach ($this->elements as &$e) {
			$method = 'get_'.$e['type'];
			if(!method_exists($this,$method)) continue;
			$this->$method($e,$data);
		}
		return $data;
	}
	public function needed() { // veraltet
		$out = array();
		foreach ($this->elements as &$e) {
			$method = 'needed_'.$e['type'];
			if(!method_exists($this,$method)) continue;
			$out = array_merge($out, $this->$method($e));
		}
		return $out;
	}
	public function filter($data) { // veraltet
		$needed = $this->needed();
		$out = array();
		foreach ($needed as $n) if (isset($data[$n])) $out[$n] = $data[$n];
		return $out;
	}
	
	private function render_hidden($e) {
		if (!isset($e['args'][0])) $e['args'][0] = '';
		return "<input type=\"hidden\" name=\"$e[name]\" value=\"{$e['args'][0]}\" id=\"$e[name]\">\n";
	}
	private function render_text($e) {
		if (!isset($e['args'][1])) $e['args'][1] = '';
		$out = "<dt><label for=\"$e[name]\">{$e['args'][0]}</label></dt>\n";
		$out .= "<dd><input type=\"text\" class=\"singleline\" name=\"$e[name]\" value=\"{$e['args'][1]}\"  size=\"30\" id=\"$e[name]\"></dd>\n";
		return $out;
	}
	private function render_password($e) {
		if (!isset($e['args'][1])) $e['args'][1] = '';
		$out = "<dt><label for=\"$e[name]\">{$e['args'][0]}</label></dt>\n";
		$out .= "<dd><input type=\"password\" name=\"$e[name]\" value=\"{$e['args'][1]}\"  size=\"30\" id=\"$e[name]\"></dd>\n";
		return $out;
	}
	private function render_textarea($e) {
		if (!isset($e['args'][1])) $e['args'][1] = '';
		$out = "<dt><label for=\"$e[name]\">{$e['args'][0]}</label></dt>\n";
		$out .= "<dd><textarea name=\"$e[name]\" rows=\"6\" cols=\"40\" id=\"$e[name]\">{$e['args'][1]}</textarea></dd>\n";
		return $out;
	}
	private function render_radio($e) {
		$out = "<dt><label>{$e['args'][0]}</label></dt>\n";
		foreach ($e['content'] as $c) {
			if (!isset($c['args'][1])) $c['args'][1] = false;
			$checked = ($c['args'][1]) ? ' checked' : '';
			$out .= "<dd>\n";
			$out .= "\t<input type=\"radio\" name=\"$e[name]\" value=\"$c[name]\" id=\"$e[name]_$c[name]\"$checked>\n";
			$out .= "\t<label for=\"$e[name]_$c[name]\">{$c['args'][0]}</label>\n";
			$out .= "</dd>\n";
		}
		return $out;
	}
	private function render_checkbox($e) {
		$out = "<dt><label>{$e['args'][0]}</label></dt>\n";
		// inform reciever that checkbox data is available even if no selection
		$out .= "<input type=\"hidden\" name=\"$e[name]\" value=\"_set\" id=\"$e[name]\">\n";
		foreach ($e['content'] as $c) {
			if (!isset($c['args'][1])) $c['args'][1] = false;
			$checked = ($c['args'][1]) ? ' checked' : '';
			$out .= "<dd>\n";
			$out .= "\t<input type=\"checkbox\" name=\"$e[name]_$c[name]\" value=\"on\" id=\"$e[name]_$c[name]\"$checked>\n";
			$out .= "\t<label for=\"$e[name]_$c[name]\">{$c['args'][0]}</label>\n";
			$out .= "</dd>\n";
		}
		return $out;
	}
	private function render_select($e) {
		$out = "<dt><label for=\"$e[name]\">{$e['args'][0]}</label></dt>\n";
		$out .= "<dd>\n";
		$out .= "\t<select size=\"1\" name=\"$e[name]\" id=\"$e[name]\">\n";
		foreach ($e['content'] as $c) {
			if (!isset($c['args'][1])) $c['args'][1] = false;
			$selected = ($c['args'][1]) ? ' selected=\"selected\"' : '';
			$out .= "\t<option value=\"$c[name]\"$selected>{$c['args'][0]}</option>\n";
		}
		$out .= "</select>\n";
		$out .= "</dd>\n";
		return $out;
	}
	
	private function set_hidden(&$e,$data) {
		$value = (isset($data[$e['name']])) ? $data[$e['name']] : '';
		$e['args'][0] = $value;
	}
	private function set_text(&$e,$data) {
		$value = (isset($data[$e['name']])) ? $data[$e['name']] : '';
		$e['args'][1] = $value;
	}
	private function set_password(&$e,$data) {
		$value = (isset($data[$e['name']])) ? $data[$e['name']] : '';
		$e['args'][1] = $value;
	}
	private function set_textarea(&$e,$data) {
		$value = (isset($data[$e['name']])) ? $data[$e['name']] : '';
		$e['args'][1] = $value;
	}
	private function set_radio(&$e,$data) {
		$value = (isset($data[$e['name']])) ? $data[$e['name']] : null;
		foreach ($e['content'] as &$c) {
			$c['args'][1] = ($value==$c['name']) ? true : false;
		}
	}
	private function set_checkbox(&$e,$data) {
		if (isset($data[$e['name']]) && $data[$e['name']]!='_set') {
			// value is not "set" by a form but coma separated values from DB
			foreach (explode(',',$data[$e['name']]) as $cname) $data[$e['name'].'_'.$cname] = 'on';
		}
		foreach ($e['content'] as &$c) {
			$c['args'][1] = (isset($data[$e['name'].'_'.$c['name']])) ? true : false;
		}
	}
	private function set_select(&$e,$data) {
		$value = (isset($data[$e['name']])) ? $data[$e['name']] : null;
		foreach ($e['content'] as &$c) {
			$c['args'][1] = ($value==$c['name']) ? true : false;
		}
	}
	
	private function get_hidden(&$e,&$data) {
		$data[$e['name']] = $e['args'][0];
	}
	private function get_text(&$e,&$data) {
		$data[$e['name']] = $e['args'][1];
	}
	private function get_textarea(&$e,&$data) {
		$data[$e['name']] = $e['args'][1];
	}
	private function get_radio(&$e,&$data) {
		$out = '';
		foreach ($e['content'] as &$c) {
			if ($c['args'][1]) $out = $c['name'];
		}
		$data[$e['name']] = $out;
	}
	private function get_checkbox(&$e,&$data) {
		$out = array();
		foreach ($e['content'] as &$c) {
			if ($c['args'][1]) $out []= $c['name'];
		}
		$data[$e['name']] = implode(',',$out);
	}
	private function get_select(&$e,&$data) {
		$data[$e['name']] = $e['args'][1];
	}
	
	private function needed_hidden(&$e) {
		return array($e['name']);
	}
	private function needed_text(&$e) {
		return array($e['name']);
	}
	private function needed_textarea(&$e) {
		return array($e['name']);
	}
	private function needed_radio(&$e) {
		return array($e['name']);
	}
	private function needed_checkbox(&$e) {
		$out = array();
		foreach ($e['content'] as &$c) {
			$out []= $e['name'].'_'.$c['name'];
		}
		return $out;
	}
	private function needed_select(&$e) {
		return array($e['name']);
	}
	
	private function compile_expression($match) {
		$element = array();
		$element['type'] = $match[1];
		$element['name'] = $match[2];
		$element['args'] = $this->arglist($match[3]);
		$element['content'] = array();
		if (isset($match[5])) {
			$in = $element['content'];
			$tmp = $this->elements;
			$this->elements = array();
			$this->compile($match[5]);
			$element['content'] = $this->elements;
			$this->elements = $tmp;
		}
		$this->elements[] = $element;
	}
	private function arglist($list) {
		if (trim($list)=='') return array();
		$list = explode(',',$list);
		foreach ($list as $k=>$v) {
			$v = trim($v);
			if ($v=='false') $v = false;
			elseif ($v=='true') $v = true;
			elseif ($v{0}=='"') {
				$v = trim($v,'"');
			} else $v = (int) $v;
			$list[$k] = $v;
		}
		return $list;
	}
}
