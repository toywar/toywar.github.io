# Compatibility monkey-patch for Ruby 3.2+ with Liquid 4.0.3
class Object
  def tainted?
    false
  end
  def untaint
    self
  end
  def taint
    self
  end
end

class String
  def tainted?
    false
  end
  def untaint
    self
  end
  def taint
    self
  end
end
