import types
from pysnmp import session
from pysnmp import error

class snmpwalk (session.session):
    """Browse remote SNMP process
    """
    def __init__ (self, agent, community):
	"""Explicitly call superclass's constructor as it gets
	overloaded by this class constructor and pass a few
	arguments alone.
	"""
	session.session.__init__ (self, agent, community)

    def run (self, objids):
	"""Query SNMP agent for one or more Object ID's. The objid
	argument should be a list of strings where each string
	represents a Object ID in dotted numbers notation
	(e.g. ['.1.3.6.1.4.1.307.3.2.1.1.1.4.1']).
	"""   
	# Convert string type Object ID's into numeric representation
	numeric_objids = map (self.str2nums, objids)

	# BER encode SNMP Object ID's to query
	encoded_objids = map (self.encode_oid, numeric_objids)

	# Since we are going to _query_ SNMP agent for Object ID's
	# associated value, there will be no variable values passed to
	# SNMP agent.
	encoded_values = []

	# traverse the agent's MIB
	while 1:
	    # Build a complete SNMP message of type 'GETNEXTREQUEST',
	    # pass it a list BER encoded Object ID's to query and an
	    # empty list of values associated with these Object IDs
	    # (empty list as there is no point to pass any variables
	    # values along the SNMP GETNEXT request)
	    question = self.encode_request ('GETNEXTREQUEST',\
	    encoded_objids, encoded_values)

	    # Try to send SNMP message to SNMP agent and receive a response.
	    answer = self.send_and_receive (question)

	    # Catch SNMP exceptions
	    try:
		# As we get a response from SNMP agent, try to disassemble
		# SNMP reply and extract two lists of BER encoded SNMP
		# Object IDs and associated values).
		(encoded_objids, encoded_values) = self.decode_response (answer)

		# SNMP agent reports 'no such name' when walk is over
	    except error.SNMPError, why:
		# If NoSuchName
		if why.status == 2:
		    # Return as we are done
		    return
		else:
		    raise error.SNMPError(why.status, why.index)

	    # Decode BER encoded Object ID.
	    objids = map (self.decode_value, encoded_objids)

	    # Decode BER encoded values associated with Object ID's.
	    values = map (self.decode_value, encoded_values)

	    # Convert two lists into a list of tuples for easier printing
	    results = map (None, objids, values)

	    # Just print them out
	    for (objid, value) in results:
		response =  response + objid + ' ---> ' + repr(value)

	    # Run the module if it's invoked for execution
if __name__ == '__main__':
    # The sys module is required for exit() function
    import sys

    # Make sure we have got enough args
    if len (sys.argv) < 4:
	# Report a usage error
	print 'Usage: %s   ' % sys.argv[0]

	# Incomplete command line arguments, exiting
	sys.exit (1)

    # Create an instance of snmpwalk class
    instance = snmpwalk (sys.argv[1], sys.argv[2])

    # Run snmpwalk against passed Object ID's and do not expect it to return
    # anything
    instance.run (sys.argv[3:])
