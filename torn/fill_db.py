import aerospike

from torn import utils
from torn.utils import parse_options

options, args = parse_options()

if __name__ == "__main__":
    config = {
        'hosts': [(options.host, options.port)]
    }

    client = aerospike.client(config).connect(
        options.username, options.password)

    namespace = options.namespace if options.namespace and options.namespace != 'None' else None
    utils.fill_db(client, namespace)
