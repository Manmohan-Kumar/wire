export class Conversation {
    constructor(
    public message: string,    
    public sender_id_fk: number,
    public receiver_id_fk: number,
    public chat_id: string,   
    public create_date?: Date,    
    ){}
}