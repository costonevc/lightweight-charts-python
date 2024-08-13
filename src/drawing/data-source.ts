import {
    Logical,
    Time,
} from 'lightweight-charts';

export interface Point {
    // Changed here, save more data in the point
    time: Time | null;
    logical: Logical;
    price: number;
    quantity: number;
    ticker: string;
    orderId: number | null;
    permId: number | null;
    clientId: number | null;
    operation: string;
}

export interface DiffPoint {
    logical: number;
    price: number;
}
