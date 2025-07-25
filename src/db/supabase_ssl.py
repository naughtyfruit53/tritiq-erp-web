import ssl

# Create SSL context for Supabase
supabase_ssl_context = ssl.create_default_context()
supabase_ssl_context.check_hostname = False
supabase_ssl_context.verify_mode = ssl.CERT_NONE