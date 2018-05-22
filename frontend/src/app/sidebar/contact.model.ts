export class Contact {
    constructor(
        public contact_id : number,
        public contact_phone_num : number,
        public contact_country_code : string,
        public user_id : number,
        public create_date : Date,
        public updated_date : Date
    ){}
}