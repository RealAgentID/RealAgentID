from agents.registry import register_agent_from_key

register_agent_from_key('coordinator', 'keys/coordinator_public.pem')
register_agent_from_key('worker-1', 'keys/worker-1_public.pem')
