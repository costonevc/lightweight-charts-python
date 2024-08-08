import {
    DeepPartial,
    MouseEventParams
} from "lightweight-charts";
import { DiffPoint, Point } from "../drawing/data-source";
import { DrawingOptions } from "../drawing/options";
import { HorizontalLine } from "./horizontal-line";

export class RayLine extends HorizontalLine {
    _type = 'RayLine';

    constructor(point: Point, options: DeepPartial<DrawingOptions>, saveDrawings: Function) {
        super({...point}, options, saveDrawings);
        this._childHandleMouseUpInteraction = this._childHandleMouseUpInteraction.bind(this);
        this._point.time = point.time;
    }

    public updatePoints(...points: (Point | null)[]) {
        for (const p of points) if (p) this._point = p;
        this.requestUpdate();
    }

    _onDrag(diff: DiffPoint) {
        this._addDiffToPoint(this._point, diff.logical, diff.price);
        this.requestUpdate();
    }

    _mouseIsOverDrawing(param: MouseEventParams, tolerance = 4) {
        if (!param.point) return false;
        const y = this.series.priceToCoordinate(this._point.price);

        const x = this._point.time ? this.chart.timeScale().timeToCoordinate(this._point.time) : null;
        if (!y || !x) return false;
        return (Math.abs(y-param.point.y) < tolerance && param.point.x > x - tolerance);
    }

    protected async _childHandleMouseUpInteraction(): Promise<void> {
        this._handleMouseUpInteraction();
        this.saveDrawings();
    }
}