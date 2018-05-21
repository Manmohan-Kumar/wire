export class Country {
    constructor(
    public iso: string,
    public name: string,
    public id?: number,
    public nicename?: Date,
    public iso3?: string,
    public numcode?: string,
    public phonecode?: string,
    public createdAt?: Date,
    public lastUpdatedBy?: string,
    ){}
}