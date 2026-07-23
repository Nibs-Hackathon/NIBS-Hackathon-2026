from database.models import AgentExecutionDB

class AgentRepository:

    def __init__(self,session):
        self.session = session

    def create(self,execution):
        self.session.add(execution)
        self.session.commit()

        self.session.refresh(execution)
        return execution

    def create_many(self, executions):
        self.session.add_all(executions)
        self.session.commit()
        return executions

    def get_all(self):
        return (
            self.session
            .query(AgentExecutionDB)
            .order_by(
                AgentExecutionDB.timestamp.desc()
            )
            .all()
        )
    def get_recent(self, limit = 20):
        return (
            self.session.query(AgentExecutionDB).order_by(AgentExecutionDB.timestamp.desc()).limit(limit).all()
        )
    def get_success_rate(self, agent_name =None):

        query =(
            self.session
            .query(AgentExecutionDB)
        )

        if agent_name:

            query = query.filter(
                AgentExecutionDB.agent_name == agent_name
            )

        executions = query.all()
        if not executions:
            return 0.0

        successful = sum(
            1
            for execution in executions
            if execution.success
        )

        return (
            successful/len(executions)
        ) * 100
    
    
        
